from constants import *
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
try:
    pygame.mixer.music.load(os.path.join('data','an-turr.ogg') )        # load music
    jumpsound = pygame.mixer.Sound( os.path.join('data','jump.wav') )   # load sound
    failsound = pygame.mixer.Sound( os.path.join('data','fail.wav') )   # load sound
except:
    raise(UserWarning, 'could not load or play soundfiles in data folder')

pygame.mixer.music.play(-1) # play non-stop
screen = pygame.display.set_mode( (640,480) )
bgsurf = pygame.Surface( screen.get_size() )
bgsurf.fill(white)
bgsurf = bgsurf.convert()
screen.blit(bgsurf, (0,0))
#pygame.display.flip(); pygame.time.wait(10000)
clock = pygame.time.Clock()
mainloop = True
while mainloop:
    miliseconds = clock.tick(fps)
    mainloop = checkQuit()
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                failsound.play()
            if e.key == pygame.K_b:
                jumpsound.play()
    pygame.display.flip()



