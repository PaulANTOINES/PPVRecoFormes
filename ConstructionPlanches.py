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
        
        self.Description = "" #exemple : PPV de (1,1) avec un seuil de 0.5, sans épuration
        self.Labels = []#labels associés de base à la bdd décision de base
        
        self.SuccessFigures = []#succès des différents chiffres (par ordre croissant)
        self.FailuresFigures = []#nb de failures des différents chiffres (ordre croissant)
        self.EvictedFigures = []#nb de mis de côté des différents chiffres (ordre croissant)
        
def essay(K,Q,seuil,nomFichier):
    #essay(1,1,0.5,"seuil05")
    #enregistrementFormatResul(K,Q,seuil,nomFichier)
    construcPlanches(nomFichier)
        
def enregistrementFormatResul(K,Q,seuil,nomFichier):
    
    (Success,Failures,Evicted,SuccessFigures,FailuresFigures,EvictedFigures) = fullProgPPV(K,Q,seuil)
    
    Description = "PPV de ("+str(K)+","+str(Q)+"), avec un seuil de " + str(seuil)
    
    txt=open('F:\ES203\BddDecisionFinal',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddDec = mon_depickler.load()
    txt.close()
    Labels = []
    for j in range(len(BddDec.Objets)):
        Labels.append(BddDec.Objets[j].label)
    
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
    
    planche0S = fabrikPlanche(Result.Success,0,Result.Labels,BddDec)
    planche1S = fabrikPlanche(Result.Success,1,Result.Labels,BddDec)
    planche2S = fabrikPlanche(Result.Success,2,Result.Labels,BddDec)
    planche3S = fabrikPlanche(Result.Success,3,Result.Labels,BddDec)
    planche4S = fabrikPlanche(Result.Success,4,Result.Labels,BddDec)
    planche5S = fabrikPlanche(Result.Success,5,Result.Labels,BddDec)
    planche6S = fabrikPlanche(Result.Success,6,Result.Labels,BddDec)
    planche7S = fabrikPlanche(Result.Success,7,Result.Labels,BddDec)
    planche8S = fabrikPlanche(Result.Success,8,Result.Labels,BddDec)
    planche9S = fabrikPlanche(Result.Success,9,Result.Labels,BddDec)
    print("premières placnhes fabriquées")
    
    registerImage("planche0S",nomFichier,planche0S)
    registerImage("planche1S",nomFichier,planche1S)
    registerImage("planche2S",nomFichier,planche2S)
    registerImage("planche3S",nomFichier,planche3S)
    registerImage("planche4S",nomFichier,planche4S)
    registerImage("planche5S",nomFichier,planche5S)
    registerImage("planche6S",nomFichier,planche6S)
    registerImage("planche7S",nomFichier,planche7S)
    registerImage("planche8S",nomFichier,planche8S)
    registerImage("planche9S",nomFichier,planche9S)
    print("premières planches save")
    
    planche0F = fabrikPlanche(Result.Failures,0,Result.Labels,BddDec)
    planche1F = fabrikPlanche(Result.Failures,1,Result.Labels,BddDec)
    planche2F = fabrikPlanche(Result.Failures,2,Result.Labels,BddDec)
    planche3F = fabrikPlanche(Result.Failures,3,Result.Labels,BddDec)
    planche4F = fabrikPlanche(Result.Failures,4,Result.Labels,BddDec)
    planche5F = fabrikPlanche(Result.Failures,5,Result.Labels,BddDec)
    planche6F = fabrikPlanche(Result.Failures,6,Result.Labels,BddDec)
    planche7F = fabrikPlanche(Result.Failures,7,Result.Labels,BddDec)
    planche8F = fabrikPlanche(Result.Failures,8,Result.Labels,BddDec)
    planche9F = fabrikPlanche(Result.Failures,9,Result.Labels,BddDec)
    
    registerImage("planche0F",nomFichier,planche0F)
    registerImage("planche1F",nomFichier,planche1F)
    registerImage("planche2F",nomFichier,planche2F)
    registerImage("planche3F",nomFichier,planche3F)
    registerImage("planche4F",nomFichier,planche4F)
    registerImage("planche5F",nomFichier,planche5F)
    registerImage("planche6F",nomFichier,planche6F)
    registerImage("planche7F",nomFichier,planche7F)
    registerImage("planche8F",nomFichier,planche8F)
    registerImage("planche9F",nomFichier,planche9F)
    print("deuxièmes planches save")
    
    planche0E = fabrikPlanche(Result.Evicted,0,Result.Labels,BddDec)
    planche1E = fabrikPlanche(Result.Evicted,1,Result.Labels,BddDec)
    planche2E = fabrikPlanche(Result.Evicted,2,Result.Labels,BddDec)
    planche3E = fabrikPlanche(Result.Evicted,3,Result.Labels,BddDec)
    planche4E = fabrikPlanche(Result.Evicted,4,Result.Labels,BddDec)
    planche5E = fabrikPlanche(Result.Evicted,5,Result.Labels,BddDec)
    planche6E = fabrikPlanche(Result.Evicted,6,Result.Labels,BddDec)
    planche7E = fabrikPlanche(Result.Evicted,7,Result.Labels,BddDec)
    planche8E = fabrikPlanche(Result.Evicted,8,Result.Labels,BddDec)
    planche9E = fabrikPlanche(Result.Evicted,9,Result.Labels,BddDec)
    
    registerImage("planche0E",nomFichier,planche0E)
    registerImage("planche1E",nomFichier,planche1E)
    registerImage("planche2E",nomFichier,planche2E)
    registerImage("planche3E",nomFichier,planche3E)
    registerImage("planche4E",nomFichier,planche4E)
    registerImage("planche5E",nomFichier,planche5E)
    registerImage("planche6E",nomFichier,planche6E)
    registerImage("planche7E",nomFichier,planche7E)
    registerImage("planche8E",nomFichier,planche8E)
    registerImage("planche9E",nomFichier,planche9E)
    print("troisièmes planches save")
    
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
                    
    
def fabrikPlanche(list,nb,Labels,Bdd):
    
    Liste = []
    planche = np.zeros((32,20,60,60))
    nbImages = 0
    for j in range(len(list)):
        if Labels[list[j]]==nb:
            nbImages+=1
            Liste.append(list[j])
    
    
    #format comme les planches de base
    k=0
    while k<nbImages:
        Ligne = k//20
        Colonne = k%20
        planche[Ligne][Colonne] = Bdd.Objets[Liste[k]].pixels
        k+=1
        print(k)
    return planche
    
    

    
