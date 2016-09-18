import pygame, sys, time, random
from pygame.locals import *
from constants import *

# rect objects for each of the four buttons
yellowrect = pygame.Rect(xmargin, ymargin, buttonsize, buttonsize)
bluerect = pygame.Rect(xmargin+buttonsize+buttongapsize, ymargin, buttonsize, buttonsize)
redrect = pygame.Rect(xmargin, ymargin+buttonsize+buttongapsize, buttonsize, buttonsize)
greenrect = pygame.Rect(xmargin+buttonsize+buttongapsize, ymargin+buttonsize+buttongapsize, buttonsize, buttonsize)

def main():
    global fpsclock, surface, basicfont,beep1,beep2,beep3,beep4
    pygame.init()
    fpsclock = pygame.time.Clock()
    surface = pygame.display.set_mode(width,height)
    pygame.display.set_caption('Simulate')
    basicfont = pygame.font.Font('freesansbold.ttf',16)
    infosurf = basicfont.render('Match the pattern by clicking on the button or using Q,W,A,S keys.',1 darkgray)
    inforect = infosurf.get_rect()
    inforect.topleft = (10,height-25)
    # load the sound files
    beep1 = pygame.mixer.sound('beep1.ogg')
    beep2 = pygame.mixer.sound('beep2.ogg')
    beep3 = pygame.mixer.sound('beep3.ogg')
    beep4 = pygame.mixer.sound('beep4.ogg')
    # initialize some variables for a new game
    pattern = [] # store the pattern of colors
    currentstep = 0 # the color the play must push next
    lastclicktime = 0 # timestamp of the player's last button push
    score = 0
    # when False, the pattern is playing, when True, waiting for the player to click a colored button
    waitingforinput = False

    while True:
        clickedbutton = True # button that was clicked ( set to yellow, red, green or blue )
        surface.fill(bgcolor)
        drawButtons()

        scoresurf = basicfont.render('Score: ' + str(score),1,white)
        scorerect = scoresurf.get_rect()
        scorerect.topleft = (width-100,10)
        surface.blit(scoresurf,scorerect)
        surface.blit(infosurf,inforect)

        checkForQuit()
        for e in pygame.event.get():
            if e.type == mousebuttonup:
                mousex,mousey = event.pos
                clickedbutton = getButtonClicked(mousex,mousey)
            elif e.type == KEYDOWN:
                if e.key == K_q: clickedbutton = yellow
                elif e.key == K_w: clickedbutton = blue
                elif e.key == K_a: clickedbutton = red
                elif e.key == K_s: clickedbutton = green
        if not waitingforinput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append( random.choice((yellow,blue,red,green)) )
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(flashdelay)
            waitingforinput = True
        else:
            # wait for the player to enter buttons
            if clickedbutton and clickedbutton == patter[currentstep]:
                # pushed the correct button
                flashButtonAnimation(clickedbutton)
                score += 1
                waitforinput = False
                currentstep = 0 # reset back to first step
            elif (clickedbutton and clickedbutton!=pattern[currentstep]) or (currentstep!=0 and time.time() - timeout > lastclicktime):
                # pushed the incorrect button or has timed out
                gameOverAnimation()
                # reset the variables
                pattern = []
                currentstep = 0
                waitingforinput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()
        pygame.display.update()
        fpsclock.tick(fps)

# --------------- helper functions ------------------------------------------------------------------
def terminate():
    pygame.quit(); sys.exit()
def checkForQuit():
    for e in pygame.event.get(QUIT):
        terminate()
    for e in pygame.event.get(KEYUP):
        if e.key == k_escape:
            terminate()
        pygame.event.post(e)
def flashButtonAnimation(color, animationspeed = 50):
    if color == yellow:
        sound = beep1
        flashcolor = brightyellow
        rectangle = yellowrect
    elif color == blue:
        sound = beep2
        flashcolor = brightblue
    elif color == red:
        sound = beep3
        flashcolor = brightred
        rectangle = redrect
    elif color == green:
        sound = beep4
        flashcolor = brightgreen
    orisurf = surface.copy()
    flashsurf = pygame.surface(buttonsize,buttonsize)
    flashsurf = flashsurf.convert_alpha()
    r,g,b = flashcolor
    sound.play()
    for start,end,step in ((0,255,1),(255,0,-1)): # animation loop
        for alpha in range(start,end,animationspeed*step):
            checkForQuit()
            surface.blit(orisurf,(0,0))
            flashsurf.fill( (r,g,b,alpha) )
            surface.blit(flashsurf,rectangle,topleft)
            pygame.display.update()
            fpsclock.tick(fps)
    surface.blit(origsurf,(0,0))

def drawButtons():
    pygame.draw.rect(surface,yellow,yellowrect)
    pygame.draw.rect(surface,blue,bluerect)
    pygame.draw.rect(surface,red,redrect)
    pygame.draw.rect(surface,green,greenrect)
def changeBackgroundAnimation(animationspeed=40):
    global bgcolor
    newbgcolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    newbgsurf = pygame.surface((width,height))
    newbgsurf = newbgsurf.convert_alpha()
    r,g,b = newbgcolor
    for alpha in range(0,255,animationspeed):
        checkForQuit()
        surface.fill(bgcolor)
        newbgsurf.fill( (r,g,b,alpha) )
        surface.blit(newbgsurf,(0,0))
        drawButtons() # redraw the buttons on top of the tint
        pygame.display.update()
        fpsclock.tick(fps)
    bgcolor = newbgcolor

def gameOverAnimation(color=white, animationspeed=50):
    orisurf = surface.copy()
    flashsurf = pygame.Surface(surface.get_size())
    flashsurf = flashsurf.convert_alpha()
    beep1.play()
    beep2.play()
    beep3.play()
    beep4.play()
    r,g,b = color
    for in in range(3): # do the flash 3 times
        for start, end ,step in ((0,255,1),(255,0,-1)):
            # the first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0
            for alpha in range(start,end,animationspeed*step): 
                # alpha means transparency, 255 is opaque, 0 is invisible
                checkForQuit()
                flashsurf.fill((r,g,b,alpha))
                surface.blit(origsurf,(0,0))
                surface.blit(flashsurf,(0,0))
                drawButtons()
                pygame.display.update()
                fpsclock.tick(fps)
def getButtonClicked(x,y):
    if yellowrect.collidepoint((x,y)): return yellow
    elif bluerect.collidepoint((x,y)): return blue
    elif redrect.collidepoint((x,y)): return red
    elif greenrect.collidepoint((x,y)): return green
    return None

if __name__ == '__main__':
    main()

