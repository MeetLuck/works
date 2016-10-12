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
clock = pygame.time.Clock()
mainloop = True
while mainloop:
    if pygame.mixer.music.get_busy(): # indicate if music is playing
        print '... music is playing'
    else:
        print '... music is not playing'
    print 'please press key:'
    print '[a] to play jump.wav sound'
    print '[b] to play fail.wav sound'
    print '[m] to toggle music on/off'
    print '[q] to quit'

    answer = raw_input('press A or B or M or Q: ')
    answer = answer.lower()
    print 'you press %s' %answer

    if 'a' in answer:
        jumpsound.play()
        print 'playing jump.wav once'
    elif 'b' in answer:
        failsound.play()
        print 'playing fail.wav once'
    elif 'm' in answer:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play()
    elif 'q' in answer:
        mainloop = False
    else:
        print 'please press either A,B,M or Q'
print 'exiting...'
pygame.quit()
