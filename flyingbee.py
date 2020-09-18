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
GROUNDY = int(SCREENHEIGHT*0.8)


def iscollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY-25 or playery < 0:
        GAME_AUDIO['hit'].play()
        return True
    
    pipeHeight=GAME_SPRITES["PIPE"][0].get_height()
    for pipe in upperPipes:
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES["PIPE"][0].get_width()):
            GAME_AUDIO['hit'].play()
            return True
            
    
    for pipe in lowerPipes:
        pipeHeight=GAME_SPRITES["PIPE"][0].get_height()
        if (playery + GAME_SPRITES["Player"].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES["PIPE"][0].get_width():
            GAME_AUDIO['hit'].play()
            return True
    return False
        


def pipegenerator():

    pipehgt=GAME_SPRITES["PIPE"][0].get_height()
    offset=SCREENHEIGHT/3
    
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES["Base"].get_height()-1.2*offset))
    playerx=SCREENWIDTH+10
    y1=pipehgt+offset-y2

    pipe=[
        {"x":playerx, "y": -y1},    #for Upper Pipe
        {"x":playerx, "y": y2}    #for Lower Pipe
    ]
    return pipe
    
def scoreDisplay():
    SCREEN.blit(GAME_SPRITES["Gameover"],(int((SCREENWIDTH - 1.2*GAME_SPRITES["Gameover"].get_width())),int((SCREENHEIGHT - 7.5*GAME_SPRITES["Gameover"].get_height()))))
    pygame.display.update()
    FPSCLOCk.tick(FPS)
    while True:

        for event in pygame.event.get():                #to get events that are taking place like pressing any key
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                return
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                return

    

def maingame():
    score=0
    playery=int(SCREENWIDTH/5)
    playerx=int(SCREENWIDTH/2)

    #Creating two new pipe to display on screen
    newpipe1=pipegenerator()
    newpipe2=pipegenerator()

    #list of Upper Pipes
    upperPipes=[
        {"x":SCREENWIDTH+200, "y":newpipe1[0]["y"]},
        {"x":SCREENWIDTH+200 + (SCREENWIDTH/2), "y":newpipe1[0]["y"]}
    ]
    #list of Lower Pipes
    lowerPipes=[
        {"x":SCREENWIDTH+200, "y":newpipe1[1]["y"]},
        {"x":SCREENWIDTH+200 + (SCREENWIDTH/2), "y":newpipe1[1]["y"],}
    ]

    pipeVelX=-4             #setting pipe velocity on x coordinate

    playerVelY=-9           #setting player velocity when it fall down
    playerMaxVelY=10        #player ki maximum velocity on Y
    playerMinVelY=8         #player ki min velocity on Y

    playerAccY=1            #player ka Acceleration

    playerFlappAcc= -8      #player Acceleration while flapping
    playerFlapped=False     #it is true when bee flapps

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type==KEYDOWN and (event.key==K_UP or event.key==K_SPACE):
                if playery > 0 :
                    playerVelY=playerFlappAcc
                    playerFlapped=True
                    GAME_AUDIO["wing"].play()
            
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if playery > 0 :
                    playerVelY=playerFlappAcc
                    playerFlapped=True
                    GAME_AUDIO["wing"].play()
        
        #to check crash with pipe or screen
        crashtest=iscollide(playerx, playery, upperPipes, lowerPipes)
        if crashtest:
            scoreDisplay()
            return

        #to check score
        playerMidPos=playerx + (GAME_SPRITES["Player"].get_width()/2)

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + int((GAME_SPRITES["PIPE"][0].get_width())/2)
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score=score+1
                print(f"Your Score Is {score}")
                GAME_AUDIO["point"].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped=False         #so that after each input it fall down

        playerheight=GAME_SPRITES["Player"].get_height()

        playery= playery + min(playerVelY, GROUNDY - playery - playerheight)

        # Move pipe to left
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe["x"]+=pipeVelX
            lowerPipe["x"]+=pipeVelX

        #to add pipe when a pipe is about to remove
        if 0 <upperPipes[0]["x"] < 5:
            newpipe=pipegenerator()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #to remove pipe when it is out of screen
        if upperPipes[0]["x"] < -GAME_SPRITES["PIPE"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #blitting all images
        SCREEN.blit(GAME_SPRITES["Background"],(0,0))
        SCREEN.blit(GAME_SPRITES["Player"],(playerx,playery))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES["PIPE"][0], (int(upperPipe["x"]),int(upperPipe["y"])))
            SCREEN.blit(GAME_SPRITES["PIPE"][1], (int(lowerPipe["x"]),int(lowerPipe["y"])))
        SCREEN.blit(GAME_SPRITES["Base"],(0,GROUNDY))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES["Numbers"][digit].get_width()

        Xoffset = int((SCREENWIDTH - width)/2)

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES["Numbers"][digit],(Xoffset, int(SCREENHEIGHT*0.12)))
            Xoffset += GAME_SPRITES["Numbers"][digit].get_width()

        pygame.display.update()
        FPSCLOCk.tick(FPS) 


def welcomeDisplay():
    
    playerx = int(SCREENWIDTH/2.5)      #setting coordinate of images wrt screen
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
            
            elif (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                return
            elif (event.type == pygame.MOUSEBUTTONDOWN):
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
        
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    
    GAME_SPRITES["Message"] = pygame.image.load('data/sprites/message.png').convert_alpha()
    GAME_SPRITES["Background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES["Player"] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES["Base"] = pygame.image.load('data/sprites/base.png').convert_alpha()
    GAME_SPRITES["Gameover"] = pygame.image.load('data/sprites/gameover.png').convert_alpha()

    GAME_AUDIO['die'] = pygame.mixer.Sound('data/audio/die.wav')
    GAME_AUDIO['hit'] = pygame.mixer.Sound('data/audio/hit.wav')
    GAME_AUDIO['point'] = pygame.mixer.Sound('data/audio/point.wav')
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound('data/audio/swoosh.wav')
    GAME_AUDIO['wing'] = pygame.mixer.Sound('data/audio/wing.wav')

    while True:
        welcomeDisplay()
        maingame()
        #welcomeDisplay()

