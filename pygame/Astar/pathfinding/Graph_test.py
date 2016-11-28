from Graph import *

pygame.init()
resolution = 640,480
screen = pygame.display.set_mode(resolution)
screen.fill(bgcolor)
g = Graph(grid)
search = Search(g,'A','T')
search.reset()
search.render()
for i in range(40):
    search.step()
    search.draw(screen)
    pygame.display.flip()
    pygame.time.wait(200)
#   search.step()
#   print g.labels
#   for node in g.nodes:
#       print node
