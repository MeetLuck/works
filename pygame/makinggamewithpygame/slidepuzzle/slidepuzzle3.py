from Component import *
import winsound

def main():
    pygame.init()
    surface = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Slide Puzzle')
    fpsclock = pygame.time.Clock()

    mainboard = Board(surface)
    while True:
        slideTo = None
        if mainboard.isSolved():
            print 'Solved'
            winsound.Beep(random.randint(5,20)*50,100)

        surface.fill(bgcolor)
        mainboard.drawBoard(surface)

        checkForQuit()

        if checkForKeyUp(): 
            slideTo = checkForKeyUp()
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONUP:
                boardpos = mainboard.converToBoardPos(e.pos[0],e.pos[1])
                if boardpos == boardPos(None,None):
                    pass
                else: # check if the clicked tile was next to the blank spot
                    blank = mainboard.getBlankTile()
                    if boardpos.x == blank.x + 1 and boardpos.y == blank.y:
                        slideTo = left
                    elif boardpos.x == blank.x - 1 and boardpos.y == blank.y:
                        slideTo = right
                    elif boardpos.x == blank.x and boardpos.y == blank.y + 1:
                        slideTo = up
                    elif boardpos.x == blank.x and boardpos.y == blank.y -1:
                        slideTo = down
        if slideTo:
            winsound.Beep(1000,10)
            mainboard.makeMove(slideTo)
            mainboard.sequence.append(slideTo) # record the slide
        pygame.display.update()
        fpsclock.tick(fps)

# --------------------------------- helper fuctions ----------------------------
def checkForQuit():
    for e in pygame.event.get(QUIT):
        pygame.quit(); sys.exit()
def checkForKeyUp():
    slideTo = None
    for e in pygame.event.get(KEYUP):
        if e.key == K_ESCAPE:           pygame.quit(); sys.exit()
        elif e.key in (K_LEFT,K_a):     slideTo = left
        elif e.key in (K_RIGHT,K_d):    slideTo = right
        elif e.key in (K_UP,K_w):       slideTo = up
        elif e.key in (K_DOWN,K_s):     slideTo = down
        pygame.event.post(e)
    return slideTo

if __name__ == '__main__':
    main()
