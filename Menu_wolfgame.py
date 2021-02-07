import pygame
import sys
import os
import random
import time
import subprocess
 

mainClock = pygame.time.Clock()
pygame.init()
#BG
surfaceW, surfaceH = 550,550
BG = pygame.transform.scale(pygame.image.load(os.path.join("assests","bannerrr.png")),(surfaceW,surfaceH))    
WIN = pygame.display.set_mode((surfaceW, surfaceH))



class Menu :

    """ Création et gestion des boutons d'un menu """

    def __init__(self, application, *groupes) :
        self.couleurs = dict(normal=(255, 255, 255),survol=(255,0,0),)
        font = pygame.font.SysFont('Helvetica', 24, bold=True)
        # noms des menus et commandes associées
        items = (('JOUER', application.jeu),('QUITTER', application.quitter))
        x = 275
        y = 430
        self._boutons = []
        for texte, cmd in items :
            mb = MenuBouton(texte,self.couleurs['normal'],font,x,y,200,50,cmd)
            self._boutons.append(mb)
            y += 80
            for groupe in groupes :
                groupe.add(mb)
 
    def update(self, events) :
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        for bouton in self._boutons :
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur) :
                # Changement du curseur par un quelconque
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche :
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else :
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
 
    def detruire(self) :
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # initialisation du pointeur
 
 
 
class MenuBouton(pygame.sprite.Sprite) :
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande) :
        super().__init__()
        self._commande = commande
 
        self.image = pygame.Surface((largeur, hauteur))
 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)
 
        self.dessiner(couleur)
 
    def dessiner(self, couleur) :
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)

 
    def executerCommande(self) :
        # Appel de la commande du bouton
        self._commande()
 
 
class Jeu :
    """ Simulacre de l'interface du jeu """
    def __init__(self, jeu, *groupes) :
        self._fenetre = jeu.fenetre
        jeu.fond = (0, 0, 0)
 
        from itertools import cycle
        couleurs = [(0, 48, i) for i in range(0, 256, 15)]
        couleurs.extend(sorted(couleurs[1:-1], reverse=True))
        self._couleurTexte = cycle(couleurs)
 
        self._font = pygame.font.SysFont('Helvetica', 36, bold=True)
        self.creerTexte()
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (surfaceW/2, surfaceH/2)
        # Création d'un event
        self._CLIGNOTER = pygame.USEREVENT + 1
        pygame.time.set_timer(self._CLIGNOTER, 80)
 
    def creerTexte(self) :
        self.texte = self._font.render(
            'LE JEU EST EN COURS D\'EXÉCUTION',
            True,
            next(self._couleurTexte)
        )
 
    def update(self, events) :
        #self._fenetre.fill(self.texte, self.rectTexte)
        subprocess.Popen("py jeu_Loup.py") #!!!!!!!!!!!!!!
        # process = subprocess.Popen("py jeu_Loup.py") #!!!!!!!!!!!!!!
        pygame.quit()
        # pygame.display.flip()
        chemin = os.getcwd()

        # chemin2  = chemin+"\\jeu_Loup.py"
        # print("chemin2 : ",chemin2)

        #subprocess.Popen([chemin+"\\jeu_Loup.py"])
        self._fenetre.blit(self.texte, self.rectTexte) 
        for event in events :
            if event.type == self._CLIGNOTER :
                self.creerTexte()
                break
 
    def detruire(self) :
        pygame.time.set_timer(self._CLIGNOTER, 0) # désactivation du timer
 
 
class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self) :
        pygame.init()

        pygame.display.set_caption("Wolf game")
        icone = pygame.image.load('assests/wolficone.png')
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assests","banner.png")),(surfaceW,surfaceH))    
        pygame.display.set_icon(icone)
 
        #self.fond = (150,)*3
        banner = pygame.image.load(os.path.join("assests","banner.png"))
 
        self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pygame.sprite.Group()
        self.statut = True
 
    def _initialiser(self) :
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass
 
    def menu(self) :
        # Affichage du menu
        self._initialiser()
        self.ecran = Menu(self, self.groupeGlobal)
 
    def jeu(self) :
        # Affichage du jeu
        self._initialiser()
        self.ecran = Jeu(self, self.groupeGlobal)
 
    def quitter(self) :
        self.statut = False
    
    
 
    def update(self) :
        events = pygame.event.get()
        WIN.blit(BG,(0,0))
        for event in events :
            if event.type == pygame.QUIT :
                self.quitter()
                return
 
        #self.fenetre.fill(self.fond)
        self.fenetre.blit(BG,(0,0))
        self.ecran.update(events)
        self.groupeGlobal.update()
        self.groupeGlobal.draw(self.fenetre)
        pygame.display.update()
        
 
 
app = Application()
app.menu()
 
clock = pygame.time.Clock()
 
while app.statut :
    app.update()
    clock.tick(30)
 
pygame.quit()