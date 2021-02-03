#!/usr/bin/env python
# coding: utf-8

# In[1]:


import  sys, os
import numpy as np
from random import randint
import random
import contextlib

with contextlib.redirect_stdout(None): # permet de ne pas afficher le hello pygmame 
    import pygame
    from pygame.locals import *

# dimensions de la fenetre 
HEIGHT = 550#175 

WIDTH = 550#175 

class Grid(object):
    
    def __init__(self):
        super(Grid, self).__init__()

        self.grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1]
        ]

        #self.grid  = [[0] * 5] * 5
        #self.grid[0][4] = 1
        # Starting position
        self.y = 2
        self.x = 0

        self.actions = [
            [-1, 0], # Up action 0
            [1, 0], #Down action 1
            [0, -1], # Left action 2
            [0, 1] # Right action 3
        ]

        self.actions2 = [
            [0,-deplacement], # Up
            [0, deplacement], #Down
            [-deplacement, 0], # Left
            [deplacement, 0] # Right
        ]

    def reset(self):
        """
            Reset world
        """
        self.y = 0
        self.x = 0
        return 1 #(self.y*3+self.x+1)

    def step(self, action):
        """
            Action: 0, 1, 2, 3
        """

        self.y = max(0, min(self.y + self.actions[action][0],4))
        self.x = max(0, min(self.x + self.actions[action][1],4))

        return (self.y*5+self.x+1) , self.grid[self.y][self.x]

    # return l'état suivant 
    def step2(self, action, loup):
        """
            Action: 0, 1, 2, 3
        """
        print("action :",action)
        loup.position.y = max(0, min(loup.position.y + self.actions2[action][1],440)) #1 0
        loup.position.x = max(0, min(loup.position.x + self.actions2[action][0],440)) #0 0
        pygame.time.wait(125)


    def show(self):
        """
            Show the grid
        """
        print("---------------------")
        y = 0
        for line in self.grid:
            x = 0
            for pt in line:
                print("%s\t" % (pt if y != self.y or x != self.x else "X"), end="")
                x += 1
            y += 1
            print("")

    def is_finished(self):
        return self.grid[self.y][self.x] == 1

    def is_finished2(self,loup):
        return self.grid[self.y][self.x] == 1 or (loup.position.x == 440 and loup.position.y == 440)

def take_action(st, Q, eps):
    # Take an action
    if random.uniform(0, 1) < eps:
        action = randint(0, 3)
    else: # Or greedy action
        action = np.argmax(Q[st]) 
        # print("action : ", np.argmax(Q[st]))
        # print("Q[st] : ",Q[st], "\n")

    return action

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



# def collides(sprite1,sprite2): 
#     sprite1_group = pygame.sprite.RenderUpdates() #this creates a render updates group, as the sprite collide function requires one of its arguments to be a group. 
#     sprite1_group.add(sprite1) 
#     collisions = pygame.sprite.spritecollide(sprite2, sprite1_group, False) #runs spritecollide, specifying the sprite, the group, and the last parameter, which should almost always be false. 
#     for other in collisions: 
#      if other != sprite2:  #spritecollide registers a sprites collision with itself, so this filters it 
#       return True 

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
                if sprite == '1':          #m = Mur
                    fenetre.blit(mur, (x,y))
                elif sprite == '0':        #d = Départ
                    fenetre.blit(vide, (x,y))
                num_case += 1
            num_ligne += 1




deplacement = 110

 # Q = 8*49 
class Chat(Perso):

    def __init__(self, x, y,  y2, x2, img="img/chat3.png"):

        
        Perso.__init__(self,x,y,img)
        
        self.y2 = y2
        self.x2 = x2

        # @arg ent = grille 
        # @arg event = evenement
    def joueurC(self, event, env):
        print("chat pos x,y = (",self.position.x,self.position.y,")")
        
        #Action: 0 haut , 1 bas , 2 gauche , 3 droite
        

        if event.type == KEYDOWN:
           

            if event.key == K_DOWN: #Si "flèche bas"
                    
                    #si le perso n'est pas tout en bas 
                    if self.position.y < HEIGHT/1.5: 

                        #On descend le perso
                        self.step(1,env)
                        self.position = self.position.move(0,deplacement) 
                        
              
            if event.key == K_UP:   #Si "flèche haut"

                #print("pos y: ",self.position.y) 
                
                # si le perso n'est pas tout en haut
                if self.position.y > 0:
                    #le perso monte
                    self.position = self.position.move(0,-deplacement)
                    self.step(0,env)
                    

            if event.key == K_LEFT: #Si "flèche gauche"
                    self.step(2,env)
                    #si le perso n'est pas tout à gauche
                    if self.position.x > 0:
                    # le perso tourne à gauche
                       self.position = self.position.move(-deplacement,0)   
                       #print("pos x: ",self.position.x) 
                       

            if event.key == K_RIGHT: #Si "flèche droite"
                    #print("pos x: ",self.position.x) 
                    self.step(3,env)
                    #si le perso n'est pas tout à gauche
                    if self.position.x < WIDTH/1.5:
                       self.position = self.position.move(deplacement,0)   

                       
            env.show()
            print(env.grid)
            #input()

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
        self.position.x = 440
        self.position.y = 440

    def step(self, action,env):
        """
            Action: 0 haut , 1 bas , 2 gauche , 3 droite
        """
        #env.grid[self.y][self.x] == 0
    
        

        y2 = max(0, min(self.y2 + env.actions[action][0],4))
        x2 = max(0, min(self.x2 + env.actions[action][1],4))
        # si la maison ne passe pas devant un mure
        if env.grid[y2][x2] != -1:

            env.grid[self.y2][self.x2] = 0
            self.y2 = y2
            self.x2 = x2 
            env.grid[self.y2][self.x2] = 1
            


class Loup(Perso):
    def __init__(self, x, y, img="img/loup.png"):

        return Perso.__init__(self,x,y,img)

    def joueurL(self, event):
        print("loup pos x,y = (",self.position.x,self.position.y,")")
        #print("pos y: ",self.position.y) 
        if event.type == KEYDOWN:

            if event.key == K_s: #Si "flèche bas"
                    
                #si le perso n'est pas tout en bas 
                if self.position.y < HEIGHT/1.5: 
                    #On descend le perso
                    self.position = self.position.move(0,deplacement)
                    
            if event.key == K_z:   #Si "flèche haut"

                # si le perso n'est pas tout en haut
                if self.position.y > 0:
                    #le perso monte
                    self.position = self.position.move(0,-deplacement)
                    

            if event.key == K_q: #Si "flèche gauche"
                
                    #si le perso n'est pas tout à gauche
                if self.position.x > 0:
                    # le perso tourne à gauche
                    self.position = self.position.move(-deplacement,0)   
                        #print("pos x: ",self.position.x) 

            if event.key == K_d: #Si "flèche droite"
                #print("pos x: ",self.position.x)     
                    #si le perso n'est pas tout à gauche
                if self.position.x < WIDTH/1.5:
                   self.position = self.position.move(deplacement,0)  

    def reset_position(self):
        self.position.x = 0
        self.position.y = 0

def collision(perso1,perso2):
    #print("loup : ("perso1.position.x,",",perso1.position.y")")
    if perso1.position.x == perso2.position.x and perso1.position.y == perso2.position.y:
        print("collision")
        return True

    return False


env = Grid()
st = env.reset()

Q = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

for _ in range(2000):
    # Reset the game
    st = env.reset()
    while not env.is_finished():
        #print("ok")
        #env.show()
        #at = int(input("$>"))
        at = take_action(st, Q, 0.4) # recuperer val max de Q

        stp1, r = env.step(at)
        #print("s", stp1)
        #print("r", r)

        # Update Q function
        atp1 = take_action(stp1, Q, 0.1)
        Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

        st = stp1

for s in range(1, 26):
    print(s, Q[s]) 

print(env.grid)

# input()
# test
st = env.reset()

groupe = pygame.sprite.Group()
    
pygame.init()
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((HEIGHT, WIDTH))

# création et chargement de la grille
fond = pygame.image.load("img/grille.png").convert()


#creation des persos
chat = Chat(440,440, y2=4,x2=4)  #HEIGHT-30,WIDTH-30)
loup = Loup(0,0) #5,4

# groupe.add(chat)
# groupe.add(loup)
# groupe.add(fond)

fenetre.blit(fond, (0,0))
fenetre.blit(chat.skin, chat.position)
fenetre.blit(loup.skin, loup.position)
#Rafraîchissement de l'écran
pygame.display.flip()

pygame.key.set_repeat(400, 30)

clock = pygame.time.Clock()



continuer = 1

total_step = 0

# niveau = Niveau('level1.txt')
# niveau.generer()
nbCollisions = 0
#BOUCLE INFINIE 
while 1 or not env.is_finished2(loup):
    fenetre.fill(pygame.Color("black"))

    clock.tick(30)
    #chat.mouvement_circulaire()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():    #Attente des événements
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])): # on appuye sur alt+f4 pour quitter
            exit()

        chat.joueurC(event,env)
        loup.joueurL(event)

    total_step += 1 

    at = take_action(st, Q, 0.4)

    env.step2(at, loup)

    env.show()

    print("loup x,y : ",loup.position.x, "," , loup.position.y)
    stp1, r = env.step(at)

    d = max(abs(chat.x2 - env.x), np.absolute(chat.y2 - env.y))

    print("d :", d)
    print("r :", r)

    if d ==0: 
        r = 100
    elif d == 1:
        print("à coté") 
        # input()  
    # else:
    #     r = 0

    atp1 = take_action(stp1, Q, 0.1)
    Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

    st = stp1


    if  collision(loup,chat):
        nbCollisions +=1
        print("nbCollisions : ",nbCollisions)
        loup.reset_position()
        chat.reset_position()
        st = env.reset()

    # if nbCollisions >= 5:
    #     fond = pygame.image.load("img/win.jpg")
    #     fenetre.blit(fond, (0,0))
    #     # chat = None
    #     print("ok win")
        # input()

    #performance = nbCollisions/total_step
    
    #print("performance : ", performance) 
    else:  
        fenetre.blit(fond, (0,0))
        fenetre.blit(chat.skin, chat.position)
        fenetre.blit(loup.skin, loup.position)

    
    #Rafraichissement
    pygame.display.flip()