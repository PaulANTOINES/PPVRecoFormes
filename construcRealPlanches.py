from PIL import Image
from PIL.Image import open as openim
from PIL.Image import new as newed
import pickle
import matplotlib.pyplot as plt
import numpy
import numpy as np
import time


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

class Resultat:
    def __init__(self):
        self.Success = []#position des labels réussis
        self.Failures = []#position des labels échoués
        self.Evicted = []#position des labels refusés
        self.Labels = []#labels associés aux décisions (format : [[position,labelDécidé]]
        
        self.Description = "" #exemple : PPV de (1,1) avec un seuil de 0.5, sans épuration
        
        
        self.SuccessFigures = []#succès des différents chiffres (par ordre croissant)
        self.FailuresFigures = []#nb de failures des différents chiffres (ordre croissant)
        self.EvictedFigures = []#nb de mis de côté des différents chiffres (ordre croissant)
        
def essay(K,Q,seuil,nomFichier):
    #essay(5,3,9,"ppvAmelio53")
    enregistrementFormatResul(K,Q,seuil,nomFichier)
    construcPlanches(nomFichier)
        
def enregistrementFormatResul(K,Q,seuil,nomFichier):
    
    (Success,Failures,Evicted,Labels,SuccessFigures,FailuresFigures,EvictedFigures) = fullProgPPV(K,Q,seuil)
    
    Description = "PPV de ("+str(K)+","+str(Q)+"), avec un seuil de " + str(seuil)
    
   
    
    resultNew = Resultat()
    
    resultNew.Success = Success
    resultNew.Failures = Failures
    resultNew.Evicted = Evicted
    resultNew.Description = Description
    resultNew.Labels = Labels
    resultNew.SuccessFigures = SuccessFigures
    resultNew.FailuresFigures = FailuresFigures
    resultNew.EvictedFigures = EvictedFigures
    
    
    txt=open('F:\ES203\\' + str(nomFichier),"wb")
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(resultNew) 
    txt.close()
    
    
        
def construcPlanches(nomFichier):#attention, à changer si on prend en compte l'éviction
    
    path = 'F:\ES203\\' + str(nomFichier)
    
    txt=open(path,"rb")
    mon_depickler = pickle.Unpickler(txt)
    Result = mon_depickler.load()#format Resultat
    txt.close()
    
    txt=open('F:\ES203\BddDecisionFinal',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddDec = mon_depickler.load()
    txt.close()
    print(Result.Labels)
    planche0D = fabrikPlancheD(0,Result.Labels,BddDec)
    planche1D = fabrikPlancheD(1,Result.Labels,BddDec)
    planche2D = fabrikPlancheD(2,Result.Labels,BddDec)
    planche3D = fabrikPlancheD(3,Result.Labels,BddDec)
    planche4D = fabrikPlancheD(4,Result.Labels,BddDec)
    planche5D = fabrikPlancheD(5,Result.Labels,BddDec)
    planche6D = fabrikPlancheD(6,Result.Labels,BddDec)
    planche7D = fabrikPlancheD(7,Result.Labels,BddDec)
    planche8D = fabrikPlancheD(8,Result.Labels,BddDec)
    planche9D = fabrikPlancheD(9,Result.Labels,BddDec)
    print("premières planches fabriquées")
    
    registerImage("planche0D",nomFichier,planche0D)
    registerImage("planche1D",nomFichier,planche1D)
    registerImage("planche2D",nomFichier,planche2D)
    registerImage("planche3D",nomFichier,planche3D)
    registerImage("planche4D",nomFichier,planche4D)
    registerImage("planche5D",nomFichier,planche5D)
    registerImage("planche6D",nomFichier,planche6D)
    registerImage("planche7D",nomFichier,planche7D)
    registerImage("planche8D",nomFichier,planche8D)
    registerImage("planche9D",nomFichier,planche9D)
    print("premières planches save")
    
    plancheEvicted = fabrikPlancheE(Result.Evicted,BddDec)
    registerImage("plancheEvicted",nomFichier,plancheEvicted)
    print("deuxièmes planches save")
    
    
    
def registerImage(nomPlanche,nomFichier,planche):
    
    im = Image.new("RGB", (1280, 2048), "white")
    pixels = im.load()
    for j in range(32):
        for k in range(20):
            for i in range(60):
                for h in range(60):
                    
                    if planche[j][k][i][h]==0:
                        
                        pixels[k*60+i,j*60+h] = (0,0,0) # set the colour accordingly
                    else:
                        pixels[k*60+i,j*60+h] = (255,255,255)
                        
    im.save('F:\ES203\\' + nomFichier + "_" + str(nomPlanche) + ".jpg")
                    
    
def fabrikPlancheD(nb,Labels,Bdd):
    
    Liste = []
    planche = np.ones((32,20,60,60))
    nbImages = 0
    for j in range(len(Labels)):
        print(Labels[j])
        if Labels[j][1]==nb:
                  
            nbImages+=1
            Liste.append(Labels[j][0])
            
    
    #format comme les planches de base
    k=0
    while k<nbImages:
        Ligne = k//20
        Colonne = k%20
        planche[Ligne][Colonne] = Bdd.Objets[Liste[k]].pixels
        k+=1
        #print(k)
    return planche
    
def fabrikPlancheE(Evicted,BddDec):
    
    
    planche = np.zeros((32,20,60,60))
    
    
    #format comme les planches de base
    k=0
    while k<len(Evicted):
        Ligne = k//20
        Colonne = k%20
        planche[Ligne][Colonne] = BddDec.Objets[Evicted[k]].pixels
        k+=1
        #print(k)
    return planche
    
