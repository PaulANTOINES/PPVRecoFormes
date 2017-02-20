from PIL import Image
from PIL.Image import open as openim
from PIL.Image import new as newed
import pickle
import matplotlib.pyplot as plt
import numpy
import numpy as np
import time



##Classes des vecteurs des jeux de tests
class resultTests:
    def __init__(self):
        self.test = [] #liste des différents caractères

class caracTests:
    def __init__(self):
        self.Komor = []#vecteur de longueur à définir en fonction du nombre de zones découpées, de base : 3 -> 135 tests
        
        #self.SondesHor = [] #vecteur de longueur à définir en fonction du nombre de zones découpées, de base : 3 -> 3 tests (moyenne à chaque fois)
        #self.SondesVert = []#vecteur de longueur à définir en fonction du nombre de zones découpées, de base : 2 -> 2 tests (moyenne à chaque fois)
        #self.pres = None #% de présence d'écriture
         
        self.label = None
        self.largeur = 64
        
        

def distanceAutre(point,Points,K):
    #Points : liste de point sous forme de resultTests puis caracTests
    
    DistPoints = []#distance des K plus proches points de point
    Labels = [] #labels associés
    
    
    taille = np.shape(Points.test[0].Komor)
    #point = np.reshape(point,taille[0]*taille[1])
    
    #vectors = np.zeros((len(Points.test),taille[0]*taille[1]))
    
    vectors = np.zeros((len(Points.test),taille[0]))
    
    for k in range(len(Points.test)):
        #vectors[k] = np.reshape(Points.test[k].Komor,taille[0]*taille[1])
        vectors[k] = Points.test[k].Komor
    
    dist = numpy.linalg.norm(vectors-point, axis = 1)
    #print(dist,np.shape(dist))
    
    while len(DistPoints)<K:
        
        ind_min = numpy.argmin(dist)
        mini = numpy.ndarray.min(dist)
        
        DistPoints.append(mini)
        Labels.append(Points.test[ind_min].label)
        
        dist = np.delete(dist,ind_min)
        
    return DistPoints,Labels

    
def decision(DistPoints,Labels,Q,threshold):
    #retourne None si on ne peut pas prendre de décision
    
    #Q : méthode de décision
    
    #à régler avec des tests
    
    #on peut utiliser le palier soit avec l'élem le plus loin, soit en faisant la moyenne des distances des éléments, soit sur le premier
    #sur le premier :
    #print(DistPoints,Labels)
    mini = min(DistPoints)
    if mini>threshold:
        return "notFound",DistPoints[0]
    #else:
    
    nb = np.zeros((10))
    
    for k in range(len(Labels)):
        nb[Labels[k]]+=1  

    max = numpy.ndarray.max(nb)
    lab = numpy.argmax(nb)

    if max>=Q:
        
        return lab,DistPoints[0]
    else:
        
        return "notFound",DistPoints[0]

        
    
def fullProgPPV(K,Q,palier):
    x = time.clock()
    
    #epurationBDD(K,Q,palier)
    
    
    #ouverture de la base d'appentissage
    txt=open('F:\ES203\BaseApprentissage',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()

    #ouverture de la base de décision
    txt=open('F:\ES203\BaseDecision',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddDec = mon_depickler.load()
    txt.close()
    
    nbReussite = 0
    refuse = 0
    reussiteParChiffre = [0,0,0,0,0,0,0,0,0,0]
    tailleNbChiffres = [0,0,0,0,0,0,0,0,0,0]
    nbRefuse = [0,0,0,0,0,0,0,0,0,0]
    nbFailure = [0,0,0,0,0,0,0,0,0,0]
    avancement = 0
    distanceTotale = 0
    Success = []
    Failures = []
    Evicted = []
    Lab = []
    
    for j in range(len(BddDec.test)):
        
        #(DistPoints,Labels) = distancesMin(BddDec.test[j].Komor,BddApp,K)
        (DistPoints,Labels) = distanceAutre(BddDec.test[j].Komor,BddApp,K)
        (label,dist) = decision(DistPoints,Labels,Q,palier)
        distanceTotale+=dist
        if label=="notFound":
            refuse+=1
            nbRefuse[BddDec.test[j].label]+=1
            Evicted.append(j)
        
        elif label == BddDec.test[j].label:
            nbReussite+=1
            reussiteParChiffre[label]+=1
            Success.append(j)
            Lab.append([j,label])
        else:
            Failures.append(j)
            nbFailure[BddDec.test[j].label]+=1
            Lab.append([j,label])
            
        tailleNbChiffres[BddDec.test[j].label]+=1
        
        
        avancement+=1
        #if j%10==0:
            #print("Avancement : " + str(round((avancement/len(BddDec.test))*100,2)) + "%")
        #if j>100:
            #print(reussiteParChiffre,nbRefuse)
            #return 2
        
    temps = time.clock()-x
    
    #distanceTotale /= len(BddDec.test)
    #print(distanceTotale)
    #Res.append([nbReussite/(len(BddDec.test)-refuse),refuse/len(BddDec.test),K,Q,temps,tailleNbChiffres,reussiteParChiffre,nbRefuse])
    
    
    
    #affichage des résultats :
    afficheResult(nbReussite/(len(BddDec.test)-refuse),refuse/len(BddDec.test),K,Q,temps,tailleNbChiffres,reussiteParChiffre,nbRefuse)
    #return (Success,Failures,Evicted,Lab,reussiteParChiffre,nbFailure,nbRefuse)
    
    
def afficheResult(pourcentage,refuse,K,Q,temps,tailleNbChiffres,reussiteParChiffre,nbRefuse):
    
    print("PPV effectuée avec un nombre de voisins de " + str(K) + " et un quorum de " + str(Q) +" : ")
    print("Pourcentage de réussite : " + str(pourcentage))
    print("Pourcentage d'exclusion : " + str(refuse))
    print("Temps d'exécution (s) : " + str(temps))
    print(" ")
    print("Statistiques en fonction des chiffres déchiffrés : ")
    for j in range(10):
        print(" ")
        print(" Chiffre : " + str(j))
        print("     Nombre total de " + str(j) + " : " + str(tailleNbChiffres[j]))
        print("     Pourcentage de réussite de " + str(j) + " : " + str(reussiteParChiffre[j]/(tailleNbChiffres[j]-nbRefuse[j])))
        print("     Pourcentage de refus de " + str(j) + " : " + str(nbRefuse[j]/tailleNbChiffres[j]))

def testting(seuil):
    #testting(5)
    fullProgPPV(1,1,seuil)
    
    fullProgPPV(2,2,seuil)
    
    fullProgPPV(3,2,seuil)
    fullProgPPV(3,3,seuil)
    
    fullProgPPV(4,2,seuil)
    fullProgPPV(4,3,seuil)
    
    fullProgPPV(5,2,seuil)
    fullProgPPV(5,3,seuil)
    
    fullProgPPV(6,2,seuil)
    fullProgPPV(6,3,seuil)
    fullProgPPV(6,4,seuil)

    fullProgPPV(7,2,seuil)
    fullProgPPV(7,3,seuil)
    fullProgPPV(7,4,seuil)
    
    fullProgPPV(8,2,seuil)
    fullProgPPV(8,3,seuil)
    fullProgPPV(8,4,seuil)
    fullProgPPV(8,5,seuil)

        
        
def epurationBDD(K,Q,palier):
    #réalise une ppv (1,1) qui épure la base d'apprentissage, pour virer les points non fiables (les trop isolés seuls seront supprimés)
    x = time.clock()
    #ouverture de la base d'appentissage
    txt=open('F:\ES203\BaseApprentissage',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()

    avancement = 0
    print(len(BddApp.test))
    j=0
    changed = 0
    while j<len(BddApp.test):
        pointEtudie = BddApp.test[j]
        
        
        (DistPoints,Labels) = distanceAutreEpuration(pointEtudie.Komor,BddApp,K)
        (label,dist) = decision(DistPoints,Labels,Q,palier)
        
        if label=="notFound":
            de  = 4
            #BddApp.test = np.delete(BddApp.test,j)
        
        else:
            if label!=pointEtudie.label:
                BddApp.test[j].label = label
                changed+=1
        j+=1
        
        
        
        avancement+=1
        #if j%10==0:
            #print("Avancement : " + str(round((avancement/len(BddApp.test))*100,2)) + "%")
        
    print("changed : " + str(changed))
    print("temps : " + str(time.clock()-x))
    print("taille finale : " + str(len(BddApp.test)))
    
    txt=open('F:\ES203\BaseApprentissageEpuree',"wb")
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddApp) 
    txt.close()
    
        
        
def distanceAutreEpuration(point,Points,K):
    #Points : liste de point sous forme de resultTests puis caracTests
    
    DistPoints = []#distance des K plus proches points de point
    Labels = [] #labels associés
    
    
    taille = np.shape(Points.test[0].Komor)
    point = np.reshape(point,taille[0]*taille[1])
    
    vectors = np.zeros((len(Points.test),taille[0]*taille[1]))
    for k in range(len(Points.test)):
        vectors[k] = np.reshape(Points.test[k].Komor,taille[0]*taille[1])
        
    
    dist = numpy.linalg.norm(vectors-point, axis = 1)
    i=0
    ff = False
    while i <np.shape(dist)[0] and ff==False:
        if dist[i]==0:
            dist = np.delete(dist,i)
            ff=True
        i+=1
            
    #print(dist,np.shape(dist))
    
    while len(DistPoints)<K:
        
        ind_min = numpy.argmin(dist)
        mini = numpy.ndarray.min(dist)
        
        DistPoints.append(mini)
        Labels.append(Points.test[ind_min].label)
        
        dist = np.delete(dist,ind_min)
        
    return DistPoints,Labels

        
        
        
        
        
        
        
    
    
    