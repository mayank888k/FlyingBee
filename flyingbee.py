import random
import sys             #to quit programe
import pygame          
from pygame.locals import *

FPS=32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))   #TO CREATE THE SCREEN IN PYGAME
GAME_AUDIO = {}
GAME_SPRITES = {}
PLAYER =  'data/sprites/bird.png'
BACKGROUND = 'data/sprites/background.png'
PIPE = 'data/sprites/pipe.png'

def welcomeDisplay():
    
    playerx = int(SCREENWIDTH/5)      #setting coordinate of images wrt screen
    playery = int((SCREENHEIGHT - GAME_SPRITES['Player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['Message'].get_width())/2)
    messagey = int((SCREENHEIGHT*0.173 ))
    basex = 0
    basey = int(0.8*SCREENHEIGHT)

    while True:

        for event in pygame.event.get():                #to get events that are taking place like pressing any key
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and event.key == K_UP):
                return
            else:

                SCREEN.blit(GAME_SPRITES["Background"],(0,0))            #to display images on screen
                SCREEN.blit(GAME_SPRITES["Player"],(playerx,playery))
                SCREEN.blit(GAME_SPRITES["Message"],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES["Base"],(basex,basey))

                pygame.display.update()                 #to update images on screen
                FPSCLOCk.tick(FPS)


if __name__ == "__main__":

    pygame.init()             #to initialize the pygame
    pygame.display.set_caption('Flying Bee By Mayank Kazim Harshit Manvi')
    FPSCLOCk = pygame.time.Clock()

    GAME_SPRITES['Numbers']=(

        pygame.image.load('data/sprites/0.png').convert_alpha(),
        pygame.image.load('data/sprites/1.png').convert_alpha(),
        pygame.image.load('data/sprites/2.png').convert_alpha(),
        pygame.image.load('data/sprites/3.png').convert_alpha(),
        pygame.image.load('data/sprites/4.png').convert_alpha(),
        pygame.image.load('data/sprites/5.png').convert_alpha(),
        pygame.image.load('data/sprites/6.png').convert_alpha(),
        pygame.image.load('data/sprites/7.png').convert_alpha(),
        pygame.image.load('data/sprites/8.png').convert_alpha(),
        pygame.image.load('data/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES["PIPE"]=(
        
        pygame.image.load(PIPE).convert_alpha(),
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180)
    )
    
    GAME_SPRITES["Message"] = pygame.image.load('data/sprites/message.png').convert_alpha()
    GAME_SPRITES["Background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES["Player"] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES["Base"] = pygame.image.load('data/sprites/base.png').convert_alpha()

    GAME_AUDIO['die'] = pygame.mixer.Sound('data/audio/die.wav')
    GAME_AUDIO['hit'] = pygame.mixer.Sound('data/audio/hit.wav')
    GAME_AUDIO['point'] = pygame.mixer.Sound('data/audio/point.wav')
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound('data/audio/swoosh.wav')
    GAME_AUDIO['wing'] = pygame.mixer.Sound('data/audio/wing.wav')

    while True:
        welcomeDisplay()
        #maingame()

