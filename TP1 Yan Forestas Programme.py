#
# ATTENTION : Nima_test = image()
#NE PAS METTRE D'ACCENT, MEME DANS LES COMMENTAIRES
#
# import des bibliotheques
from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class image:
    # Initialisation d'une image composee d'un tableau 2D vide
    # (pixels) et de 2 dimensions (H = height et W = width) mises a 0
    def __init__(self):
        self.pixels = None 
        self.H = 0
        self.W = 0
        
    # Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
    # et affectation des dimensions de l'image self avec les dimensions 
    # du tableau 2D (tab_pixels) 
    def set_pixels(self, tab_pixels):
        self.pixels = tab_pixels
        self.H,self.W = self.pixels.shape 

    # Lecture d'un image a partir d'un fichier de nom "file_name"
    def load_image(self, file_name):
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")

    # Affichage a l'ecran d'une image
    def display(self, window_name):
        fig=plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide")
            
    def modif_ima(self,S):
    
        im_modif = image()
        im_modif.set_pixels(np.zeros((self.H,self.W), dtype=np.uint8))
                                                
        for l in range(self.H):
            for c in range(self.W):
                if self.pixels[l][c] >= S:
                    im_modif.pixels[l][c] = 255
                else :
                    im_modif.pixels[l][c] = self.pixels[l][c]
        return im_modif
    
    
    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================

    def binaris(self,S): 
        im_modif = image()
        im_modif.set_pixels(np.zeros((self.H,self.W), dtype=np.uint8))
        for l in range(self.H):
            for c in range(self.W):
                if self.pixels[l][c] >= S:
                    im_modif.pixels[l][c] = 255
                else :
                    im_modif.pixels[l][c] = 0
        return im_modif
        
        
    
    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================

    def localisation(self):
        l_min,c_min = self.H,self.W
        l_max = 0
        c_max = 0
        for l in range(self.H):
            for c in range(self.W):
                if self.pixels[l][c] == 0:
                    if l > l_max:
                        l_max = l
                    if l < l_min:
                        l_min = l    
                    if c > c_max:
                        c_max = c
                    if c < c_min:
                        c_min = c
                        
        img = image()
        img.pixels = self.pixels[l_min:l_max+1, c_min:c_max+1]
        img.H = l_max - l_min
        img.W = c_max - c_min
        return img
    
    
    
         
    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================

    def resize_im(self,new_H,new_W):
        img = image()
        img.pixels = resize(self.pixels, (new_H,new_W), 0)
        img.H = new_H
        img.W = new_W
        img.pixels = np.uint8(img.pixels*255)
        return img



    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
   
    

    def simil_im(self,im):
        nb_pixels = len(self.pixels)*len(self.pixels[0])
        nb_pixels_correles = 0
        for k in range(len(self.pixels)):
            for z in range(len(self.pixels[0])):
                if (self.pixels[k][z] == im.pixels[k][z]):
                   nb_pixels_correles += 1 
        return nb_pixels_correles/nb_pixels



#==============================================================================
#  Fonction de lecture des fichiers contenant les images modeles
#  Les differentes images sont mises dans une liste
# l'element '0' de la liste de la liste correspond au chiffre 0,
# l'element '1' au chiffre 1, etc.
#==============================================================================

    def reconnaissance(self):
        fichiers= ['_0.png','_1.png','_2.png','_3.png','_4.png','_5.png','_6.png', 
             '_7.png','_8.png','_9.png']
        image_test = self.binaris(150)
        image_test = image_test.localisation()
        list_correlation = []
        
        for fichier in fichiers:
            model = image()
            model.load_image(fichier)
            image_aux = image_test.resize_im(model.H, model.W)
            list_correlation.append(image_aux.simil_im(model))
        
        
        ind = 0
        val = list_correlation[0]
        for k in range (1,len(list_correlation)):

            if list_correlation[k] > val:
                ind = k
                val = list_correlation[k]
        
        return ind
   
    
    def reconnaissance_mult(self):
        deja_vu_colonne_avec_noir = False
        images_numeros = []
        numeros = []
        ind = 0
        img = self.binaris(150)
        for k in range (len(self.pixels[0])):
            est_espace = True
            for z in range(len(img.pixels)):
                if img.pixels[z][k] == 0:
                    est_espace = False
                    deja_vu_colonne_avec_noir = True
                    
      
            if est_espace and deja_vu_colonne_avec_noir:
                num = image()
                num.pixels = img.pixels[0:img.H, ind : k+1]
                num.H = img.H
                num.W = k + 1 - ind
                images_numeros.append(num)
                deja_vu_colonne_avec_noir = False
                
            
            if est_espace:
                ind = k
        
        
        for k in range (len(images_numeros)):
            imag = images_numeros[k]
            numeros.append(imag.reconnaissance())
            
        return numeros
            
    
    
    
    
    
    
    
#==============================================================================
#==============================================================================

#   PROGRAMME PRINCIPAL

#==============================================================================
# # Lecture image
#==============================================================================

im = image()
im.load_image('test10.JPG')
im.display("image initiale")

 


#==============================================================================
# Binarisation
#==============================================================================



#
#==============================================================================
#  Localisation chiffre
#==============================================================================
#



#
#==============================================================================
# Test de la fonction resize
#==============================================================================




#
#==============================================================================
# Test de la fonction similitude
#==============================================================================




#==============================================================================
# Lecture des chiffres modeles
#==============================================================================

# test verifiant la bonne lecture de l'un des modeles, par exemple le modele '8'
list_model[8].display("modele 8")

#==============================================================================
# Mesure de similitude entre l'image et les modeles 
# et recherche de la meilleure similitude
#==============================================================================



image_test = image()
image_test.load_image('test8.jpg')
image_test10 = image()
image_test10.load_image('test10.jpg')
image_test10.display("e")

