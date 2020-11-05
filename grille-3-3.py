import numpy as np
from random import randint
import random
import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *

WIDTH = 280
HEIGHT = 280



class Perso(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.skin = pygame.image.load(img).convert_alpha()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.skin.get_rect();

        self.position = self.skin.get_rect()
        self.position.x = x
        self.position.y = y

class EnvGrid(object):
    """
        docstring forEnvGrid.
    """
    def __init__(self):
        super(EnvGrid, self).__init__()

        self.grid = [
            [0, 0, 1],
            [0, -1, 0],
            [0, 0, 0]
        ]
        # Starting position
        self.y = 2
        self.x = 0

        self.actions2 = [
            [0,-93], # Up
            [0, 93], #Down
            [-93, 0], # Left
            [93, 0] # Right
        ]

        self.actions = [
            [-1, 0], # Up action 0
            [1, 0], #Down action 1
            [0, -1], # Left action 2
            [0, 1] # Right action 3
        ]
    def reset(self):
        """
            Reset world
        """
        self.y = 2 # position initiales
        self.x = 0
        return (self.y*3+self.x+1) # retourne l'état 7

    
    def show(self):
        """
            Show the grid
        """
        print("---------------------")
        y = 0
        for line in self.grid: # pour chaque lignes
            x = 0
            for pt in line: # pour chaque colonnes
                
                print("%s\t" % (pt if y != self.y or x != self.x else "X"), end="") # on affiche les cellules ou X si aucun changement
                #print("\r {}".format(x), end="")
                x += 1
            y += 1
            print("")
        #time.sleep(0.5)

    def is_finished(self):
        return self.grid[self.y][self.x] == 1 # finish si etat final = etat actuel = 1

    def is_finished2(self,voiture):
        return self.grid[self.y][self.x] == 1 or (voiture.position.x == 186 and voiture.position.y == 0)

    # return l'état suivant 
    def step(self, action):
        """
            Action: 0, 1, 2, 3
        """
        self.y = max(0, min(self.y + self.actions[action][0],2)) 
        self.x = max(0, min(self.x + self.actions[action][1],2)) 

        return (self.y*3+self.x+1) , self.grid[self.y][self.x] 

    # return l'état suivant 
    def step2(self, action, voiture):
        """
            Action: 0, 1, 2, 3
        """
        print("action :",action)
        voiture.position.y = max(0, min(voiture.position.y + self.actions2[action][1],186)) #1 0
        voiture.position.x = max(0, min(voiture.position.x + self.actions2[action][0],186)) #0 0
        pygame.time.wait(125)
        


def take_action(st, Q, eps):
    # fait une action en fonction de Q
    if random.uniform(0, 1) < eps: # si la proba aléaatoire est inférieur à epsilon, on fait de l'exploration
        action = randint(0, 3) 
    else: # sinon on fait de l'expoitation
        action = np.argmax(Q[st]) # chercher dans Q la meilleur action en retournant la valeur de l'indice 
    return action



class Voiture(Perso):
    def __init__(self, x, y, img="img/voiture.png"):
        return Perso.__init__(self,x,y,img)

    def joueurV(self, event):
        #print("voiture pos x,y = (",self.position.x,self.position.y,")")
        if event.type == KEYDOWN:

            if event.key == K_DOWN: #Si "flèche bas"
                    
                    #si le perso n'est pas tout en bas 
                    if self.position.y < HEIGHT/2: 
                        #On descend le perso
                        self.position = self.position.move(0,93) 
                    
            if event.key == K_UP:   #Si "flèche haut"

                
                #print("pos y: ",self.position.y) 

                # si le perso n'est pas tout en haut
                if self.position.y > 10:
                    #le perso monte
                    self.position = self.position.move(0,-93)
                    

            if event.key == K_LEFT: #Si "flèche gauche"

                    #si le perso n'est pas tout à gauche
                    if self.position.x > 11:
                    # le perso tourne à gauche
                       self.position = self.position.move(-93,0)   
                       #print("pos x: ",self.position.x) 

            if event.key == K_RIGHT: #Si "flèche droite"
                    #print("pos x: ",self.position.x) 
                    #si le perso n'est pas tout à gauche
                    if self.position.x < 140:#WIDTH:
                       self.position = self.position.move(93,0)   


    def reset_position(self):
        self.position.x = 140
        self.position.y = 140





env = EnvGrid()
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
    [0, 0, 0, 0]
]


# entrainement
for _ in range(100):

    # Reset the game
    st = env.reset()
    while not env.is_finished():
        #print("ok")
        #env.show()
        #at = int(input("$>"))
        at = take_action(st, Q, 0.4)

        stp1, r = env.step(at)
        
        

        # Update Q function
        atp1 = take_action(stp1, Q, 0.1)

        Q[st][at] +=  0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])
        
        #input("")
        st = stp1

for s in range(1, 10):
    print(s, Q[s])



pygame.init()
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((HEIGHT, WIDTH))

fond = pygame.image.load("img/grille3-3_2.png").convert()
fenetre.blit(fond, (0,0))

#creation des persos
voiture = Voiture(0,0)

obstacle = Perso(93, 93, "img/obstacle.png")

maison = Perso(186, 0, "img/maison.png")

fenetre.blit(voiture.skin, voiture.position)
fenetre.blit(obstacle.skin, obstacle.position)
fenetre.blit(maison.skin, maison.position)
#Rafraîchissement de l'écran
pygame.display.flip()

pygame.key.set_repeat(400, 30)

clock = pygame.time.Clock()

fini = False

st = env.reset()
#BOUCLE INFINIE
continuer = 1
while continuer and not env.is_finished2(voiture):
    fenetre.fill(pygame.Color("black"))
    clock.tick(30)

    for event in pygame.event.get():    #Attente des événements
        if event.type == QUIT:
            continuer = 0

    #voiture.position.x = 186
    #voiture.position.y = 186
    # test
    

        
    # env.show()
    # print("x,y : ",env.x,",",env.y)
    #at = int(input("$>"))
    at = take_action(st, Q, 0.4)

    env.step2(at, voiture)
    print("voiture x,y : ",voiture.position.x, "," , voiture.position.y)
    env.step(at)

    fenetre.blit(fond, (0,0))
    fenetre.blit(voiture.skin, voiture.position)
    fenetre.blit(obstacle.skin, obstacle.position)

        #print("s", stp1)
        #print("r")

        # exploitation
        #atp1 = take_action(stp1, Q, 0.1)
        #Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

        #st = stp1
    #print("x,y : ",env.x,",",env.y) 

 
    
   
    voiture.joueurV(event)
    fenetre.blit(fond, (0,0))
    fenetre.blit(voiture.skin, voiture.position)
    fenetre.blit(obstacle.skin, obstacle.position)
    fenetre.blit(maison.skin, maison.position)

    #Rafraichissement
    pygame.display.flip()


    