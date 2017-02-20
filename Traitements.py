from PIL import Image
from PIL.Image import open as openim
from PIL.Image import new as newed
import pickle
import matplotlib.pyplot as plt
import numpy as np
import time
#from Komori import *
from math import *

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
        
##traitement condensé :

def totalTreatment():
    
    print("Découpage des fichiers d'apprentissage et de décision")
    decoupFichiers()
    print("Done")
    
    print("Enlevage des images blanches")
    premierTraitement()
    print("Done")
    
    print("Redécoupage des images pour n'avoir que la surface utile")
    decoupPlus()
    print("Done")
    
    print("Lancement de Komori (5 minutes d'execution...)")
    #vectTest()
    print("Done")

##Découpage des fichiers :


#découpe les images de la bdd d'apprentissage et décision sous la forme de listes de 64x64 pixels, associées à un label :

##Classes de découpage des images
class BddApprentissage:
    def __init__(self):
        self.Objets = [] #liste d'Images
        
class Images:
    def __init__(self):
        self.pixels = np.zeros((60, 60)) #liste des pixels
        self.label = None #chiffre correspondant
        
        
def decoupFichiers():
    #découpage des fichiers images d'apprentissage en objets de taille 64x64 accompagné d'un label
    ##apprentissage
    
    BddApp = BddApprentissage()
    
    
    for j in range(10):#chacune des 10 images
    
    
        #ouverture des images
        phrase = "F:\ES203\\" + "appr_"+ str(j) + ".bmp"
        print(phrase)
        im=openim(phrase)
        
        
        for i in range(32):#on parcourt les ligne
            for k in range(20):#on parcourt les colonnes
            
                ima = Images()
                #on parcourt des carrés de côté 64 : 
                for m in range(2, 62):
                    for l in range(2, 62):
                        ima.pixels[l-2][m-2] = im.getpixel((k*64+l,i*64+m))%254
                ima.label = j
                BddApp.Objets.append(ima)
                        
                    
               
    txt=open('F:\ES203\BddApprent',"wb")#on remet dans le pickle
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddApp) 
    txt.close()
    
    ##Décision
    
    BddDec = BddApprentissage()
    
    
    for j in range(10):#chacune des 10 images
    
    
        #ouverture des images
        phrase = "F:\ES203\\" + "rec_"+ str(j) + ".bmp"
        print(phrase)
        im=openim(phrase)
        
        
        for i in range(32):#on parcourt les ligne
            for k in range(20):#on parcourt les colonnes
            
                ima = Images()
                #on parcourt des carrés de côté 64 : 
                for m in range(2, 62):
                    for l in range(2, 62):
                        ima.pixels[l-2][m-2] = im.getpixel((k*64+l,i*64+m))%254
                ima.label = j
                BddDec.Objets.append(ima)
                        
                    
               
    txt=open('F:\ES203\BddDecision',"wb")#on remet dans le pickle
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddDec) 
    txt.close()
                
    
##Tri des images
#on va ici supprimer les images vides :
    
def premierTraitement():
    #Ici, on va vérifier qu'il n'y a pas de case vide ou peu utilisable 
    ##Apprentissage :
    
    txt=open('F:\ES203\BddApprent',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    print(len(BddApp.Objets))
   
    j=0
    
    
    while j<len(BddApp.Objets):
        
        
        if np.amin(BddApp.Objets[j].pixels) == 1:
            BddApp.Objets = BddApp.Objets[0:j] + BddApp.Objets[j+1:]#on enlève si vide  
            
            
        else:
            j+=1
        
                
                                                         
    print(len(BddApp.Objets))
    
    txt=open('F:\ES203\BddApprentFinal',"wb")#on remet dans le pickle
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddApp) 
    txt.close()
    
    ##Décision :
    
    txt=open('F:\ES203\BddDecision',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    
    print(len(BddApp.Objets))
    j=0
    while j<len(BddApp.Objets):
        
        
        if np.amin(BddApp.Objets[j].pixels) == 1:
            BddApp.Objets = BddApp.Objets[0:j] + BddApp.Objets[j+1:]#on enlève si vide  
        else:
            j+=1
            
                                                         
    print(len(BddApp.Objets))
    
    txt=open('F:\ES203\BddDecisionFinal',"wb")#on remet dans le pickle
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddApp) 
    txt.close()
    

    

##Découpe des images
def decoupPlus():
    #on va découper en hauteur chaque chiffre, pour accélérer le tout, et mieux pouvoir comparer des chiffres qui n'ont pas la même la taille
    #découpage horizontal en plus
    
    txt=open('F:\ES203\BddApprentFinal',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    j=0
    while j < len(BddApp.Objets):
        
        dim = zoneUtile(BddApp.Objets[j].pixels)                   
        
        BddApp.Objets[j].pixels = BddApp.Objets[j].pixels[dim[0] : dim[1] + 1 , dim[2] : dim[3] + 1]
        
        j+=1
        
    
    txt=open('F:\ES203\BddApprentTrait2',"wb")#on remet dans le pickle
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddApp) 
    txt.close()
    
    
    
    txt=open('F:\ES203\BddDecisionFinal',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    j=0
    while j < len(BddApp.Objets):
        
        dim = zoneUtile(BddApp.Objets[j].pixels)                   
        
        BddApp.Objets[j].pixels = BddApp.Objets[j].pixels[dim[0]: dim[1]+1, dim[2] : dim[3]+1]
        j+=1
        #print(j)
        
    
    txt=open('F:\ES203\BddDecisionTrait2',"wb")#on remet dans le pickle
    mon_pickler = pickle.Pickler(txt)
    mon_pickler.dump(BddApp) 
    txt.close()
    
def zoneUtile(image):

    pix_up = 0
    pix_down = 59
        
    pix_left = 0
    pix_right = 59
    
    #pixel du haut limite
    k = 0
    while(np.amin(image[k]) == 1):
        k += 1
         
    pix_up = k
        
                    
    #pixel du bas limite
    k = 0
    while(np.amin(image[pix_down - k]) == 1):
        k += 1
     
    pix_down -= k
            
      
            
    #pixel de gauche limite
    k = 0
    while(np.amin(image[:, k]) == 1):
        k += 1
         
    pix_left = k
             
    #pixel de droite limite
    k = 0
    while(np.amin(image[:, pix_right - k]) == 1):
        k += 1
            
    pix_right -= k
    
    return(np.array([pix_up, pix_down, pix_left, pix_right]))
    
def position(horizontal,vertical):
    return vertical*64+horizontal
    
def vertical(pos):
    return pos//64
    
def horizontal(pos):
    return pos%64
   
