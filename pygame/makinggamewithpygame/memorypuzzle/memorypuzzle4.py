from Component2 import *

def main():
    pygame.init()
    surface = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Memory Game')

    mainboard = Board()
    surface.fill(bgcolor)
    mainboard.startGameAnimation(surface)

    #mouseX,mouseY = 0,0  # mouse point 
    firstbox = None

    while True: # main loop
        mouseclicked = False
        surface.fill(bgcolor)
        mainboard.drawBoard(surface)

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                pygame.quit(); sys.exit()
            elif e.type == MOUSEMOTION:
                mouseX,mouseY = e.pos
            elif e.type == MOUSEBUTTONUP:
                mouseX,mouseY = e.pos
                mouseclicked = True

        # get box at current mouse point
        box = mainboard.getBoxAt(mouseX,mouseY)

        # check if the mouse is currently over a box.
        if box == None: continue 
        #-------------- mouse is over a box ---------------------------------
        if not mouseclicked and not box.revealed:
            box.drawHighlight(surface)
            pygame.display.update()
            fpsclock.tick(fps)
        if not mouseclicked or box.revealed: continue
        #-------------- box is not opened and mouse clicked -----------------
        box.revealed = True # set the box as revealeded unconditionally
        mainboard.revealBoxesAnimation(surface,(box,))
        winsound.Beep(100,20)

        if firstbox == None: # -> first box clicked
            firstbox = box
        else: # -> second box clicked
            secondbox = box
            # check if there is a match between the two icons
            if firstbox != secondbox: # icons don't match. Re-cover up both selections
                mainboard.coverBoxesAnimation(surface,(firstbox,secondbox))
                pygame.time.wait(200) # 1000 msec = 1 sec
                firstbox.revealed = secondbox.revealed = False
            elif mainboard.hasWon():
                mainboard.gameWonAnimation(surface)
                # reset board
                mainboard = Board()
                mainboard.startGameAnimation(surface)
            if firstbox == secondbox:
                winsound.Beep(500,20)
            # reset first selection variable  after second box clicked
            firstbox = None 

        # redraw the screen and wait a clock tick
        pygame.display.update()
        fpsclock.tick(fps)

if __name__ == '__main__':
    main()
