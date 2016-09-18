from Component import *
import winsound

def main():
    pygame.init()
    surface = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Slide Puzzle')
    fpsclock = pygame.time.Clock()

    reset_surf,reset_rect = makeText('Reset', textcolor, tilecolor, width-120, height-90)
    new_surf, new_rect = makeText('New Game', textcolor, tilecolor, width-120,height-60)
    solve_surf,solve_rect = makeText('Solve', textcolor, tilecolor, width-120, height-30)
    #msg_surf,msg_surf = makeText('Click tile or press arrow Keys to slide', textcolor, bgcolor, 100, 30,fontsize=24)

    mainboard = Board(surface)
    while True:
        slideTo = None
        if mainboard.isSolved():
            print 'Solved' 
            msg_surf,msg_rect = makeText( 'solved !!!', red, bgcolor, width/2 - 15 * 10/2, 50,fontsize=30)
            winsound.Beep(random.randint(5,20)*50,100)
        else:
            msg_surf,msg_rect = makeText('Click tile or press arrow Keys to slide', textcolor, bgcolor, 100, 50,fontsize=24)

        surface.fill(bgcolor)
        surface.blit(reset_surf, reset_rect)
        surface.blit(new_surf, new_rect)
        surface.blit(solve_surf, solve_rect)
        surface.blit(msg_surf, msg_rect)
        mainboard.drawBoard(surface)

        checkForQuit()

        if checkForKeyUp(): 
            slideTo = checkForKeyUp()
        for e in pygame.event.get():
            if e.type != MOUSEBUTTONUP: continue
            boardpos = mainboard.converToBoardPos(e.pos[0],e.pos[1])
            if boardpos == (None,None):
                print '....'
                # check if the user clicked on an option button
                if reset_rect.collidepoint(e.pos):
                    mainboard.resetAnimation(surface)
                    #resetAnimation(mainboard, allmoves) # clicked on Reset button
                    #allmoves = []
                elif new_rect.collidepoint(e.pos):
                    mainboard = Board(surface)
                    #mainboard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                    #allmoves = []
                elif solve_rect.collidepoint(e.pos):
                    print 'solve puzzle ...',
                    print 'e.pos'
                    mainboard.solvePuzzle(surface)
                    #resetAnimation(mainboard,solutionSeq+allmoves) # clicked on Solve button
                    #allmoves = []
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

def makeText(text,color,bgcolor,top,left,fontsize=20): # create the surface and rect objects for some text
    basicfont = pygame.font.Font('freesansbold.ttf',fontsize)
    textsurf = basicfont.render(text,True,color,bgcolor)
    textrect = textsurf.get_rect()
    textrect.topleft = (top,left)
    return (textsurf, textrect)

if __name__ == '__main__':
    main()
