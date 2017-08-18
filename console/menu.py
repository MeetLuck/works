#import unicurses as curses
from helper import *

#def wrapper(obj,*args,**kwargs):
#    try:
#        screen = curses.initscr()
#        screen.keypad(1)
#        curses.noecho(); curses.cbreak(); curses.curs_set(0)
#        curses.start_color()
#        #setattr(obj,'init_colors',init_colors)
#        obj(screen,*args,**kwargs)  # Enter the main loop
#    finally:
#        screen.clear()
#        screen.refresh()
#        screen.keypad(0)
#        curses.echo(); curses.nocbreak(); curses.curs_set(1)
#        curses.endwin()		    # Terminate curses

class Menu(object):                                                          

    def __init__(self, items, screen):                                    
        self.window,self.panel = new_panel(10,30,5,10) #screen.subwin(10,30,5,10)                                  
        curses.init_pair(6,curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.white_green = curses.color_pair(6)
        self.window.bkgd(self.white_green)
        self.window.keypad(1)                                                
        self.panel = new_panel(self.window)                            
        self.panel.hide()                                                    
        self.windows = list()
        self.windows.append(screen)
        self.windows.append(self.window)
        curses.update_panels()                                                
        curses.doupdate()

        self.position = 0                                                    
        self.items = items                                                   
        self.items.append(('exit','exit'))                                   
    def update(self):
#       for win in self.windows:
#           win.clear()
#           win.touchwin()
#           win.refresh()
        curses.update_panels()                                                
        curses.doupdate()
        #curses.doupdate()

    def navigate(self, n):                                                   
        self.position += n                                                   
        if self.position < 0:                                                
            self.position = 0                                                
        elif self.position >= len(self.items):                               
            self.position = len(self.items)-1                                

    def display(self):                                                       
        #self.panel.top()
        self.update()

        while True:                                                          
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                msg = '%d. %s' % (index, item[0])                            
                self.window.addstr(1+index, 1, msg, mode)                    

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:                         
                if self.position == len(self.items)-1:                       
                    break                                                    
                else:                                                        
                    self.items[self.position][1]()                           

            elif key == curses.KEY_UP:                                       
                self.navigate(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate(1)                                             
            self.update()
        else:
            self.update()


class MyApp(object):                                                         

    def __init__(self, screen):                                           
        #self.screen = screen                                              
        curses.curs_set(0)                                                   

        submenu_items = [                                                    
                ('beep', curses.beep),                                       
                ('flash', curses.flash)                                      
                ]                                                            
        submenu = Menu(submenu_items, screen)                           

        main_menu_items = [                                                  
                ('beep', curses.beep),                                       
                ('flash', curses.flash),                                     
                ('submenu', submenu.display)                                 
                ]                                                            
        main_menu = Menu(main_menu_items, screen)                       
        main_menu.display()                                                  

if __name__ == '__main__':                                                       
    wrapper(MyApp)   
