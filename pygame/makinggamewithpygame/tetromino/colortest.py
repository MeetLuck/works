import pygame
from pygame.locals import *
# dictionary of colors
allcolors = pygame.color.THECOLORS
colornames = allcolors.keys()
colornames.sort()

#colorfile = file('colorfile.txt','wt')
#for name in colornames:
#    print name, allcolors[name]
#    line = '%s : %s\n' %(name,allcolors[name])
#    colorfile.write(line)
#colorfile.close()

def main():
    pygame.init()
    numstring = tuple( map(str, range(0,10)) )
    print len(colornames)
    
    for name in colornames:
        if name.endswith(numstring): continue
        for e in pygame.event.get():
            checkForPause()
            #if e.type == KEYUP and e.key == K_p:
        print name, allcolors[name]
    pygame.time.wait(200)



def checkForPause():
    while True:
        if checkForKeyPress() == None:
            print 'check For Pause'
            pygame.time.wait(100)
        

def checkForKeyPress():
    print 'check For KeyPress'
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    for event in pygame.event.get(QUIT):
        pygame.quit(); sys.exit()
#   for event in pygame.event.get(KEYUP):
#       if event.key == k_escape:
#           pygame.quit();sys.exit
#       pygame.event.post(e)
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return True #event.key
    return None

if __name__ == '__main__':
    main()
