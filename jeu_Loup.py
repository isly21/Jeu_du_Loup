#!/usr/bin/env python
# coding: utf-8

# In[1]:


import  sys, os

import contextlib

with contextlib.redirect_stdout(None): # permet de ne pas afficher le hello pygmame 
    import pygame
    from pygame.locals import *

# dimensions de la fenetre 
HEIGHT = 181 #270

WIDTH = 181 #228

class Perso(pygame.sprite.Sprite):
    # @arg : x,y = position initiale de l'objet
    #        img = chemin du fichier 
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.skin = pygame.image.load(img).convert_alpha()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.skin.get_rect(center=(x, y));
        self.position = self.skin.get_rect()
        self.position.x = x
        self.position.y = y




def collides(sprite1,sprite2): 
    sprite1_group = pygame.sprite.RenderUpdates() #this creates a render updates group, as the sprite collide function requires one of its arguments to be a group. 
    sprite1_group.add(sprite1) 
    collisions = pygame.sprite.spritecollide(sprite2, sprite1_group, False) #runs spritecollide, specifying the sprite, the group, and the last parameter, which should almost always be false. 
    for other in collisions: 
     if other != sprite2:  #spritecollide registers a sprites collision with itself, so this filters it 
      return True 

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
	
	
	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""	
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau
	
	
	def afficher(self, fenetre):
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		mur = pygame.image.load("img/mur1.png")
		vide = pygame.image.load("img/carre1.png")
		
		
		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * 35
				y = num_ligne * 35
				if sprite == '1':		   #m = Mur
					fenetre.blit(mur, (x,y))
				elif sprite == '0':		   #d = Départ
					fenetre.blit(vide, (x,y))
				num_case += 1
			num_ligne += 1

 # Q = 8*49 
class Chat(Perso):
    def __init__(self, x, y, img="img/chat.png"):
        return Perso.__init__(self,x,y,img)

    def joueurC(self, event):
    	print("chat pos x,y = (",self.position.x,self.position.y,")")
    	if event.type == KEYDOWN:

            if event.key == K_DOWN: #Si "flèche bas"
                    
                    #si le perso n'est pas tout en bas 
                    if self.position.y < HEIGHT/1.5: 
                        #On descend le perso
                        self.position = self.position.move(0,35) 
                    
            if event.key == K_UP:   #Si "flèche haut"

                
                #print("pos y: ",self.position.y) 

                # si le perso n'est pas tout en haut
                if self.position.y > 10:
                    #le perso monte
                    self.position = self.position.move(0,-35)
                    

            if event.key == K_LEFT: #Si "flèche gauche"

                    #si le perso n'est pas tout à gauche
                    if self.position.x > 11:
                    # le perso tourne à gauche
                       self.position = self.position.move(-35,0)   
                       #print("pos x: ",self.position.x) 

            if event.key == K_RIGHT: #Si "flèche droite"
                    #print("pos x: ",self.position.x) 
                    #si le perso n'est pas tout à gauche
                    if self.position.x < 140:#WIDTH:
                       self.position = self.position.move(35,0)   

    def mouvement_circulaire(self):
    	
		#gauche
    	if self.position.x >= 12 and self.position.y ==198:
    		for i in range(0,9):
    			
	    		self.position = self.position.move(-i,0)
	    		print("pos y: ",self.position.y) 
	    		pygame.time.delay(100)
		#haut
    	if self.position.x <= -12 and self.position.y <=198:
    		for i in range(0,9):
    			
	    		self.position = self.position.move(0,-i)
	    		print("pos y: ",self.position.y) 
	    		pygame.time.delay(100)

    def reset_position(self):
        self.position.x = 140
        self.position.y = 140

class Loup(Perso):
    def __init__(self, x, y, img="img/loup2.png"):
        return Perso.__init__(self,x,y,img)

    def joueurL(self, event):
    	print("loup pos x,y = (",self.position.x,self.position.y,")")
    	#print("pos y: ",self.position.y) 
    	if event.type == KEYDOWN:

            if event.key == K_s: #Si "flèche bas"
                    
                #si le perso n'est pas tout en bas 
                if self.position.y < HEIGHT/1.5: 
                    #On descend le perso
                    self.position = self.position.move(0,35)
                    
            if event.key == K_w:   #Si "flèche haut"

                # si le perso n'est pas tout en haut
                if self.position.y > 4:
                    #le perso monte
                    self.position = self.position.move(0,-35)
                    

            if event.key == K_a: #Si "flèche gauche"
                
                    #si le perso n'est pas tout à gauche
                if self.position.x > 11:
                    # le perso tourne à gauche
                    self.position = self.position.move(-35,0)   
                        #print("pos x: ",self.position.x) 

            if event.key == K_d: #Si "flèche droite"
                #print("pos x: ",self.position.x)     
                    #si le perso n'est pas tout à gauche
                if self.position.x < 140:#WIDTH:
                   self.position = self.position.move(35,0)  

    def reset_position(self):
        self.position.x = 0
        self.position.y = 0

def collision(perso1,perso2):
	#print("loup : ("perso1.position.x,",",perso1.position.y")")
	if perso1.position.x == perso2.position.x and perso1.position.y == perso2.position.y:
		print("collision")
		return True

	return False


		
pygame.init()
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((HEIGHT, WIDTH))

# création et chargement de la grille
#fond = pygame.image.load("img/grille.png").convert()
#fenetre.blit(fond, (0,0))

#creation des persos
chat = Chat(140,140)  #HEIGHT-30,WIDTH-30)
loup = Loup(0,0) #5,4


fenetre.blit(chat.skin, chat.position)
fenetre.blit(loup.skin, loup.position)
#Rafraîchissement de l'écran
pygame.display.flip()

pygame.key.set_repeat(400, 30)

clock = pygame.time.Clock()


#BOUCLE INFINIE
continuer = 1

niveau = Niveau('level1.txt')
niveau.generer()


while continuer:
    fenetre.fill(pygame.Color("black"))

    clock.tick(30)
    #chat.mouvement_circulaire()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():    #Attente des événements
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])): # on appuye sur alt+f4 pour quitter
            continuer = 0

        chat.joueurC(event)
        loup.joueurL(event)
	  

        #print("collision : ",pygame.sprite.collide_mask(chat,loup))
        #loup.collide2(chat)
        #print("collides : ",collides(loup,chat))

        if(collision(loup,chat)):
        	loup.reset_position()
        	chat.reset_position()

    niveau.afficher(fenetre)  
    fenetre.blit(chat.skin, chat.position)
    fenetre.blit(loup.skin, loup.position)

    
    #Rafraichissement
    pygame.display.flip()