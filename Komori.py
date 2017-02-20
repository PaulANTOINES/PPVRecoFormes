from PIL import Image
from PIL.Image import open as openim
from PIL.Image import new as newed
import pickle
import matplotlib.pyplot as plt
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
        
class Komorii:
    def __init__(self):
        self.pos = 0
        self.bal = []
        
class BddApprentissage:
    def __init__(self):
        self.Objets = [] #liste d'Images
        
class Images:
    def __init__(self):
        self.pixels = np.zeros((60, 60)) #liste des pixels
        self.label = None #chiffre correspondant

##Jeux de test pour fichiers d'apprentissage :

def vectTest():
    x = time.clock()
    txt=open('F:\ES203\BddApprentTrait2',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    testing = resultTests()
    
    for j in range(len(BddApp.Objets)):
        new = caracTests()
        new.label = BddApp.Objets[j].label
        
        
        Kom = Komori(BddApp.Objets[j].pixels)
        SondesVert = sonderVert(BddApp.Objets[j].pixels,False)
        SondesHor = sonderHor(BddApp.Objets[j].pixels,False)
        SondesVertBas = sonderVert(BddApp.Objets[j].pixels,True)
        SondesHorDroite = sonderHor(BddApp.Objets[j].pixels,True)
        PresenceVert = presVert(BddApp.Objets[j].pixels)
        PresenceHor = presHor(BddApp.Objets[j].pixels)
        
        
        vect = np.zeros(139)
        vect[0:41] = Kom[0][0:]
        vect[41:82] = Kom[1][0:]
        vect[82:123] = Kom[2][0:]
        
        nbDeBlanc = sum(sum(BddApp.Objets[j].pixels))
        taille = np.shape(BddApp.Objets[j].pixels)
        total = taille[0]*taille[1]
        
        presence = (total - nbDeBlanc)/total
        
        #vect[123] = presence
        vect[124:126] = SondesVert[:]
        vect[126:129] = SondesHor[:]
        vect[129:131] = SondesVertBas[:]
        vect[131:134] = SondesHorDroite[:]
        #vect[134:136] = PresenceVert[:]
        #vect[136:] = PresenceHor[:]
        
        new.Komor = vect
        testing.test.append(new)
        
        
        print(j)
        
        
    txt=open('F:\ES203\BaseApprentissage',"wb")#on enregiste Bdd prise sous format pickle (pour conserver l'objet)
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(testing) 
    txt.close()
    
    
    txt=open('F:\ES203\BddDecisionTrait2',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    testing = resultTests()
    
    for j in range(len(BddApp.Objets)):
        new = caracTests()
        new.label = BddApp.Objets[j].label
        
        
        Kom = Komori(BddApp.Objets[j].pixels)
        SondesVert = sonderVert(BddApp.Objets[j].pixels,False)
        SondesHor = sonderHor(BddApp.Objets[j].pixels,False)
        SondesVertBas = sonderVert(BddApp.Objets[j].pixels,True)
        SondesHorDroite = sonderHor(BddApp.Objets[j].pixels,True)
        PresenceVert = presVert(BddApp.Objets[j].pixels)
        PresenceHor = presHor(BddApp.Objets[j].pixels)
        
        
        vect = np.zeros(139)
        vect[0:41] = Kom[0][0:]
        vect[41:82] = Kom[1][0:]
        vect[82:123] = Kom[2][0:]
        
        nbDeBlanc = sum(sum(BddApp.Objets[j].pixels))
        taille = np.shape(BddApp.Objets[j].pixels)
        total = taille[0]*taille[1]
        
        presence = (total - nbDeBlanc)/total
        
        #vect[123] = presence
        vect[124:126] = SondesVert[:]
        vect[126:129] = SondesHor[:]
        vect[129:131] = SondesVertBas[:]
        vect[131:134] = SondesHorDroite[:]
        #vect[134:136] = PresenceVert[:]
        #vect[136:] = PresenceHor[:]
        
        new.Komor = vect
        testing.test.append(new)
        
        print(j)
        
        
    txt=open('F:\ES203\BaseDecision',"wb")#on enregiste Bdd prise sous format pickle (pour conserver l'objet)
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(testing) 
    txt.close()
    
    return time.clock()-x
    
def presVert(pixels):
    taille = np.shape(pixels)
    presenceVert = np.zeros(2)
    zone1 = taille[1]//2
    zone2 = taille[1] - zone1
    
    tailleZone1 = zone1*taille[0]
    tailleZone2 = zone2*taille[0]
    
    nbZone1 = sum(sum(pixels[:][0:zone1]))
    try:
        nbZone2 = sum(sum(pixels[:][zone1:]))
    except:
        nbZone2 = 0
    
    presenceVert[0] = (tailleZone1-nbZone1)/(tailleZone1)
    presenceVert[1] = (tailleZone2-nbZone2)/(tailleZone2)
    
    
    return presenceVert
    
def presHor(pixels):
    taille = np.shape(pixels)
    presenceHor = np.zeros(3)
    zone1 = taille[0]//3
    zone2 = (taille[0]-zone1)//2
    zone3 = taille[0]-zone1-zone2
    
    tailleZone1 = zone1*taille[1]
    tailleZone2 = zone2*taille[1]
    tailleZone3 = zone3*taille[1]
    
    nbZone1 = sum(sum(pixels[0:zone1][:]))
    nbZone2 = sum(sum(pixels[zone1:zone1+zone2][:]))
    nbZone3 = sum(sum(pixels[zone1+zone2:][:]))
    
    presenceHor[0] = (tailleZone1-nbZone1)/(tailleZone1)
    presenceHor[1] = (tailleZone2-nbZone2)/(tailleZone2)
    presenceHor[2] = (tailleZone3-nbZone3)/(tailleZone3)
    
    return presenceHor

                
    
def sonderHor(pixels,droite):
    #on va lancer des sondes par le haut, sur deux zones, puis en faire la moyenne
    
    taille = np.shape(pixels)
    sondeHor = np.zeros((taille[0]))
    if droite==False:
        for j in range(taille[0]):
            sondeHor[j] = lanceSondeHor(j,pixels,taille[1])
    else:
        for j in range(taille[0]):
            sondeHor[j] = lanceSondeHorDroite(j,pixels,taille[1])
        
    zone1 = taille[0]//3
    zone2 = (taille[0]-zone1)//2
    zone3 = taille[0]-zone1-zone2
    
    moy1 = sum(sondeHor[0:zone1])/zone1
    moy2 = sum(sondeHor[zone1:zone2+zone1])/zone2
    moy3 = sum(sondeHor[zone2+zone1:])/zone3
    
    
    
    moy1 /=taille[0]
    moy2 /=taille[0]
    moy3 /=taille[0]
    
    hor = np.array([moy1,moy2,moy3])
    return hor
    
def lanceSondeHor(j,pixels,largeur):
    rangNoir = 0
    i=0
    found = False
    while i < largeur and found == False:
        if pixels[j][i]==0:
            rangNoir = i
            found = True
        i+=1
    return rangNoir
    
def lanceSondeHorDroite(j,pixels,largeur):
    rangNoir = 0
    i=0
    found = False
    while i < largeur and found == False:
        if pixels[j][largeur-i-1]==0:
            rangNoir = i
            found = True
        i+=1
    return rangNoir
    
    
def sonderVert(pixels,bas):
    #on va lancer des sondes par le haut, sur deux zones, puis en faire la moyenne
    
    taille = np.shape(pixels)
    sondeVert = np.zeros((taille[1]))
    if bas==False:
        for j in range(taille[1]):
            sondeVert[j] = lanceSondeVert(j,pixels,taille[0])
    else:
        for j in range(taille[1]):
            sondeVert[j] = lanceSondeVertBas(j,pixels,taille[0])
        
    zone1 = taille[1]//2
    zone2 = taille[1] - zone1
    
    moy1 = sum(sondeVert[0:zone1])/zone1
    moy2 = sum(sondeVert[zone1:])/zone2
    
    moy1 /=taille[0]
    moy2 /=taille[0]
    
    vert = np.array([moy1,moy2])
    return vert
    
def lanceSondeVert(j,pixels,hauteur):
    rangNoir = 0
    i=0
    found = False
    while i < hauteur and found == False:
        if pixels[i][j]==0:
            rangNoir = i
            found = True
        i+=1
    return rangNoir
    
def lanceSondeVertBas(j,pixels,hauteur):
    rangNoir = 0
    i=0
    found = False
    while i < hauteur and found == False:
        if pixels[hauteur-i-1][j]==0:
            rangNoir = i
            found = True
        i+=1
    return rangNoir
        
    

def Komori(pixels):
    #en entrée : tableau de pixels de l'image, dimensionnée selon le découpage
    #sortie : liste des densités de présence des 45 classes dans 3 zones (plus ou moins précise)
    #améliorations : pas faire uniquement des densité, demander d'autres trucs, ajouter longueur et largeur à chaque fois ( base : 64x64) -> zones : 21/22/21 
    
    #1ere étape : étiquetage
    #classes : 
    #représentation initiale : tableau de 3x3, case centrale en None si blanc, True si noir, les autres en True ou False
    
    taille = np.shape(pixels)
    
    listKom = np.zeros((taille[0], taille[1]))#liste des différentes balises (komori) des points de la liste pixels
    
    for i in range(taille[0]):
        for j in range(taille[1]):
            balise = lancerSonde(i, j, pixels)
            listKom[i, j] = classe(balise)
        
    
    #2eme étape : éclatage de la classe full True (à faire?)
    
    
    #3eme : définition des 3 zones (hauteur n'est pas forcément divisible par 3
    
    zone1 = taille[0]//3
    zone2 = (taille[0]-zone1)//2
    zone3 = taille[0]-zone1-zone2
    
    
    #4eme : densités sur les différentes zones
    Densite = np.zeros((3, 41)) #41 classes différentes sur chacune des 3 zones
    
    
    
    #zone1:
    for i in range(zone1):#lignes
        for j in range(taille[1]):#colonnes
            nb_balise = listKom[i , j]
            if nb_balise != 42:                
                Densite[0, nb_balise -1]+=1
                
                
    #zone2:
    for i in range(zone2):#lignes
        for j in range(taille[1]):#colonnes
            nb_balise = listKom[i + zone1, j]
            if nb_balise != 42:
                Densite[1, nb_balise - 1]+=1
                
                
    #zone3:
    for i in range(zone3):#lignes
        for j in range(taille[1]):#colonnes
            nb_balise = listKom[i + zone1 + zone2, j]
            if nb_balise != 42:
                Densite[2, nb_balise -1]+=1
    
    zone1Blanc = nbrBlancs(0,zone1,pixels, taille[1])
    zone2Blanc = nbrBlancs(zone1,zone1+zone2,pixels, taille[1])
    zone3Blanc = nbrBlancs(zone2+zone1,zone2+zone1+zone3,pixels, taille[1])
    
    #print("Ceci est le nb de pixels blancs en zone 1:" + str(zone1Blanc),zone1)
    #print("Ceci est le nb de pixels blancs en zone 2:" + str(zone2Blanc),zone2)
    #print("Ceci est le nb de pixels blancs en zone 3:" + str(zone3Blanc),zone3)
    #if zone3Blanc == 0 :
        #print(Densite)
    try:
        Densite[0] *= 1/zone1Blanc
    except:
        print("de")
    try:
        Densite[1] *= 1/zone2Blanc
    except:
        print("de")
    try:
        Densite[2] *= 1/zone3Blanc          
    except:
        print("de")
                
    return Densite#vecteur de taille 123
            

def nbrBlancs(ligne_debut, ligne_fin, pixels, largeur):
    nbBlancs = 0
    vect_test = np.ones((1, ligne_fin - ligne_debut))
    vect_dot = np.ones((largeur, 1))
    nbBlancs = np.dot(np.dot(vect_test, pixels[ligne_debut : ligne_fin]) , vect_dot)
    return(int(nbBlancs[0]))
    
def lancerSonde(x, y , image):
    
    taille = np.shape(image)
    
    balise = [[False,False,False],[False,None,False],[False,False,False]]
    
    if image[x, y]==0:#si on tombe sur de l'écriture, on ne fait pas le traitement
        balise[1][1] = True
        return balise
        
    #haut :
    j = x - 1
    while balise[0][1] == False and j >= 0 :#on va parcourir les points des lignes juste au dessus du point (que l'on commence par le haut ou par le point, cela ne change rien)
        if image[j][y]==0:
            balise[0][1] = True
        j -= 1
            
    #bas
    j = x + 1
    while balise[2][1] == False and j < taille[0] :#on va parcourir les points des lignes juste au dessus du point (que l'on commence par le haut ou par le point, cela ne change rien)
        if image[j][y]==0:
            balise[2][1] = True
        j += 1
            
    #gauche
    j = y - 1
    while balise[1][0] == False and j >= 0 :
        if image[x, j]==0:
            balise[1][0] = True
        j -= 1
            
    #droite
    j = y + 1
    while balise[1][2] == False and j < taille[1] :
        if image[x, j]==0:
            balise[1][2] = True
        j += 1
            
    #haut gauche
    i = x - 1
    j = y - 1
    while balise[0][0] == False and i >= 0 and j >= 0:
        if image[i][j]==0:
            balise[0][0] = True
        i -= 1
        j -= 1
            
    #haut droite
    i = x - 1
    j = y + 1
    while balise[0][2] == False and i >= 0 and j < taille[1]:
        if image[i][j]==0:
            balise[0][2] = True
        i -= 1
        j += 1
            
    #bas droite
    i = x + 1
    j = y + 1
    while balise[2][2] == False and i < taille[0] and j > taille[1]:
        if image[i][j]==0:
            balise[2][2] = True
        i += 1
        j += 1
            
    #bas gauche
    i = x + 1
    j = y - 1
    while balise[2][0] == False and i < taille[0] and j >= 0:
        if image[i][j]==0:
            balise[2][0] = True
        i += 1
        j -= 1
            
    return balise
   
    
def classe(balise):
    
    #•all True
    if balise == [[True,True,True],[True,None,True],[True,True,True]]:
        return 1
        
    #one False :
    elif balise == [[False,True,True],[True,None,True],[True,True,True]]:
        return 2
    elif balise == [[True,False,True],[True,None,True],[True,True,True]]:
        return 3
    elif balise == [[True,True,False],[True,None,True],[True,True,True]]:
        return 4
    elif balise == [[True,True,True],[False,None,True],[True,True,True]]:
        return 5
    elif balise == [[True,True,True],[True,None,False],[True,True,True]]:
        return 6
    elif balise == [[True,True,True],[True,None,True],[False,True,True]]:
        return 7
    elif balise == [[True,True,True],[True,None,True],[True,False,True]]:
        return 8
    elif balise == [[True,True,True],[True,None,True],[True,True,False]]:
        return 9
        
    #two False :    
    elif balise == [[False,False,True],[True,None,True],[True,True,True]]:
        return 10
    elif balise == [[True,False,False],[True,None,True],[True,True,True]]:
        return 11
    elif balise == [[True,True,False],[True,None,False],[True,True,True]]:
        return 12
    elif balise == [[True,True,True],[True,None,False],[True,True,False]]:
        return 13
    elif balise == [[True,True,True],[True,None,True],[True,False,False]]:
        return 14
    elif balise == [[True,True,True],[True,None,True],[False,False,True]]:
        return 15
    elif balise == [[True,True,True],[False,None,True],[False,True,True]]:
        return 16
    elif balise == [[False,True,True],[False,None,True],[True,True,True]]:
        return 17
        
    #three False :
    elif balise == [[False,False,False],[True,None,True],[True,True,True]]:
        return 18
    elif balise == [[True,False,False],[True,None,False],[True,True,True]]:
        return 19
    elif balise == [[True,True,False],[True,None,False],[True,True,False]]:
        return 20
    elif balise == [[True,True,True],[True,None,False],[True,False,False]]:
        return 21
    elif balise == [[True,True,True],[True,None,True],[False,False,False]]:
        return 22
    elif balise == [[True,True,True],[False,None,True],[False,False,True]]:
        return 23
    elif balise == [[False,True,True],[False,None,True],[False,True,True]]:
        return 24
    elif balise == [[False,False,True],[False,None,True],[True,True,True]]:
        return 25
    
    #four False:
    elif balise == [[False,False,False],[True,None,False],[True,True,True]]:
        return 26
    elif balise == [[True,False,False],[True,None,False],[True,True,False]]:
        return 27
    elif balise == [[True,True,False],[True,None,False],[True,False,False]]:
        return 28
    elif balise == [[True,True,True],[True,None,False],[False,False,False]]:
        return 29
    elif balise == [[True,True,True],[False,None,True],[False,False,False]]:
        return 30
    elif balise == [[False,True,True],[False,None,True],[False,False,True]]:
        return 31
    elif balise == [[False,False,True],[False,None,True],[False,True,True]]:
        return 32
    elif balise == [[False,False,False],[False,None,True],[True,True,True]]:
        return 33
        
    #five False
    elif balise == [[False,False,False],[True,None,False],[True,True,False]]:
        return 34
    elif balise == [[True,False,False],[True,None,False],[True,False,False]]:
        return 35
    elif balise == [[True,True,False],[True,None,False],[False,False,False]]:
        return 36
    elif balise == [[True,True,True],[False,None,False],[False,False,False]]:
        return 37
    elif balise == [[False,True,True],[False,None,True],[False,False,False]]:
        return 38
    elif balise == [[False,False,True],[False,None,True],[False,False,True]]:
        return 39
    elif balise == [[False,False,False],[False,None,True],[False,True,True]]:
        return 40
    elif balise == [[False,False,False],[False,None,False],[True,True,True]]:
        return 41
        
    else:
        return 42