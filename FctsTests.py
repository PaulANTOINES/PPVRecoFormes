from PIL import Image
from PIL.Image import open as openim
from PIL.Image import new as newed
import pickle
import matplotlib.pyplot as plt
import numpy



def visualisationApp(nb):
    
    txt=open('F:\ES203\BddApprentFinal',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()

    
    imtest(BddApp.Objets[nb].pixels,64,64)
    
def imtest(L,hauteur,largeur):
    img = newed( 'RGB', (int(largeur),int(hauteur)), "black") # create a new black image
    pixels = img.load() # create the pixel map
    
    
    for o in range(hauteur):    # for every pixel:
        for y in range(largeur):
            if L[y,o]==0:
                pixels[y,o] = (0,0,0) # set the colour accordingly
            else:
                pixels[y,o] = (255,255,255)
            
    
    img.show()
    
    
def affiche(rang):
    
    txt=open('F:\ES203\BddApprentTrait2',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    
    taille = np.shape(BddApp.Objets[rang].pixels)
    #largeur = BddApp.Objets[rang].largeur 
    #hauteur = int(len(BddApp.Objets[rang].pixels)/BddApp.Objets[rang].largeur)
    print(taille)
    imtest(BddApp.Objets[rang].pixels,taille[1],taille[0])
    
def parcours():
    txt=open('F:\ES203\BaseDecision',"rb")
    mon_depickler = pickle.Unpickler(txt)
    BddApp = mon_depickler.load()
    txt.close()
    count = 0
    for k in range(len(BddApp.test)):
        if BddApp.test[k].label==None:
            count+=1
    return count
    
    
    