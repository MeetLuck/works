from parts2 import *

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.type == pygame.MOUSEMOTION:
            self.mousepos = event.pos
#           print 'mouse over', self.mousepos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousepos = event.pos
            self.mouseclicked = True
#           print 'self.mousepos %s' %self.mouseclicked
    def render(self):
        self.screen.fill(bgcolor)
        self.board.drawBoard(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()

    def isMouseOver(self,box):
        return box != None

    def mainloop(self):
        firstbox = None
        while self.running:
            self.mouseclicked = False
            self.render()
            for event in pygame.event.get():
                self.onEvent(event)
            # get a box at current mouse point
            box = self.board.getBoxAt(self.mousepos)
            # check if the mouse is currently over a box
            if not self.isMouseOver(box): continue
            # mouse is over a box
            if not self.mouseclicked and not box.revealed:
#               print 'mouse not clicked a box but box not revealed'
                box.drawHighlight(self.screen)
                pygame.display.flip()
                clock.tick(fps)
            if not self.mouseclicked or box.revealed:
#               print 'mouse not clicked or box opened'
                continue
#           if box.revealed: continue
#           elif not box.revealed:
#               if not self.mouseclicked:
#                   box.drawHighlight(self.screen)
#                   pygame.display.flip()
#                   clock.tick(fps)
#                   continue
            # box is not opened and mouse clicked
            box.revealed = True
            print 'start reveal boxes animation'
            self.board.revealBoxesAnimation(self.screen, (box,) )
            winsound.Beep(100,20)
            if firstbox is None: # 1st box clicked
                print 'box is 1st box',box.shape
                firstbox = box
            else: # 2nd box clicked
                print 'box is 2nd box',box.shape
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
            clock.tick(fps)
        self.quit()
if __name__ == '__main__':
    App().mainloop()
