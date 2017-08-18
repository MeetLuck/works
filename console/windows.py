from helper import *

class myWin(object):
    def __init__(self,screen):
        self.screen = screen
        self.height,self.width = curses.LINES, curses.COLS
        self.init_colors()
        nrows,ncols,top,left = 10, 50, 5,5 
        self.window = newwin(nrows,ncols,top,left)
        self.window.bkgd(self.brightred)
        self.status = newwin(3,self.width-2,self.height-3,1)
        self.status.bkgd(self.blue)
        self.status.addstr('Press ESC to quit')
        self.windows = list()
        self.windows.append(screen)
        self.windows.append(self.window)
        self.windows.append(self.status)
        self.mainloop()

    def update(self):
        for win in self.windows:
            win.refresh()

    def mainloop(self):
        self.running = True
        while self.running:
            self.update()
            key = self.screen.getch()
            if key == 27: self.running = False
            self.window.addch(5,10,key)#,self.red)

if __name__ == '__main__':
    wrapper(myWin)
