import pygame
import sys
import os
import random
import time

pygame.font.init()

mainClock = pygame.time.Clock()
pygame.init()
#BG
WIDTH, HEIGHT= 550,550
BG = pygame.transform.scale(pygame.image.load(os.path.join("assests","banner.png")),(WIDTH,HEIGHT)) 
PLAY = pygame.transform.scale(pygame.image.load(os.path.join("assests","playy.png")),(70,70)) 

#donner un titre à la fenêtre 
pygame.display.set_caption("Wolf Game")
#definir l'icone de la fenêtre 
icone = pygame.image.load('assests/wolficone.png')
pygame.display.set_icon(icone)
#définir la taille de la fenêtre
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()
font = pygame.font.SysFont(None,20)

#charger les images
play = pygame.image.load(os.path.join("assests","playy.png"))

#pour que la fenêtre générer reste active

run = True
FPS = 60
level = 1
lives = 5
main_font = pygame.font.SysFont("comicsans",50)
clock = pygame.time.Clock()
def draw_text(text,font,color,x,y):
	textobj = font.render(text,1,color)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
click = False
def main_menu():
	while True:
		screen.fill((0,0,0))
		draw_text('main_menu',font,(255,255,255),screen,20,20)

		mx,my = pygame.mouse.get_pos()

		button_1 = pygame.Rect(50,100,200,50)
		button_2 = pygame.Rect(50,200,200,50)

		if button_1.collidepoint((mx,my)) : 
			if click :
				game()
		if button_2.collidepoint((mx,my)) : 
			if click :
				options()

		pygame.draw.rect(screen,(255,0,0),button_1)
		pygame.draw.rect(screen,(255,0,0),button_2)

		click = False

		for event in pygame.event.get() :
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN :
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN :
				if event.button == 1:
					click = True
		pygame.display.update()
		mainClock.tick(60)

def game():
	running = True 
	while running:
		screen.fill((0,0,0))
		draw_text('game',font,(255,255,255),screen,20,20)
		for event in pygame.event.get() :
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN :
				if event.key == K_ESCAPE:
					running = False

		pygame.display.update()
		mainClock.tick(60)
def options():
	running = True 
	while running:
		screen.fill((0,0,0))
		draw_text('options',font,(255,255,255),screen,20,20)
		for event in pygame.event.get() :
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN :
				if event.key == K_ESCAPE:
					running = False

		pygame.display.update()
		mainClock.tick(60)


def redraw_window():
	#appliquer l arrière plan du jeu 
	WIN.blit(BG,(0,0))
	WIN.blit(PLAY,(240,460))
	#mise à jour de l écran
	pygame.display.update()
	#draw text
	lives_label = main_font.render(f"Lives :{lives}", 1,(255,255,255))
	level_label = main_font.render(f"Level : {level}",1,(255,255,255))

	WIN.blit(lives_label,(10,10))
	WIN.blit(level_label,(WIDTH - level_label.get_width() - 10,10)) 



while run :
	
	clock.tick(FPS)
	redraw_window()
	pygame.display.flip()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()

