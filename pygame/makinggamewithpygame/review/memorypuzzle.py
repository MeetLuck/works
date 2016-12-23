from parts import *

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Memory Puzzle Game')
        self.screen.fill(bgcolor)
        self.board = Board()
        self.board.startGameAnimation(self.screen)
        self.running = True
    def onEvent(self,event):
        if event.type == pygame.KEYDOWN and event.key = pygame.K_ESCAPE:
            self.running = False
        elif event.type = pygame.MOUSEMOTION:
            self.mousepos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousepos = event.pos
            self.mouseclicked = True
    def render(self):
        self.screen.fill(bgcolor)
        self.board.drawBoard(self.screen)

    def quit(self):
        pygame.quit()

    def mainloop(self):
        firstbox = None
        while self.running:
            self.mouseclicked = False
            for event in pygame.event.get():
                self.onEvent(event)
            # get a box at current mouse point
            box = self.board.getBoxAt(*self.mousepos)
            # check if the mouse is currently over a box
            if box == None: continue
            # mouse is over a box
            if box.revealed: continue
            elif not box.revealed:
                if not self.mouseclicked:
                    box.drawHighlight(self.screen)
                    pygame.display.flip()
                    fpsclock.tick(fps)
                    continue
            # box is not opened and mouse clicked
            box.revealed = True
            self.board.revealBoxesAnimation(self.screen, (box,) )
            winsound.Beep(100,20)
            if firstbox == None: # 1st box clicked
                firstbox = box
            else: # 2nd box clicked
                secondbox = box
                # check if there is a match between the two icons
                if firstbox != secondbox: # icons not match, re-cover up both selections
                    self.board.coverBoxesAnimation(self.screen, (firstbox,secondbox) )
                    pygame.time.wait(200) # msec
                    firstbox.revealed = secondbox.revealed = False
                elif self.board.hasWon():
                    self.board.gameWonAnimation(self.screen)
                    # reset board
                    self.board = Board()
                    self.board.startGameAnimation(self.screen)
                if firstbox == secondbox:
                    winsound.Beep(500,20)
                # reset first selection after 2nd box clicked
                firstbox = None
            self.render()
        self.quit()
if __name__ == '__main__':
    App().mainloop()
