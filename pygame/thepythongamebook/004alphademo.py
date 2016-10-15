''' 004 alphademo.py
colorkey and alpha-value
'''
import pygame,os
white = pygame.Color('white')

# image.set_alpha(alpha)
# if you have a pygame surface WITHOUT IN-BUILTIN TRANSPARENCY such as an .JPG image
# you can set an alpha-value(transparency) for the whole surface with set_alpha

def get_alpha_surface(surf,alpha=128,R=128,G=128,B=128,mode=pygame.BLEND_RGBA_MULT):
    # returns a copy of a surface object with user defined values from R,G,B and Alpha
    # using this blit mode, you can make an image all blue, red or green by setting
    # the Per-Pixel-Alpha values for the corresponding color
    alphasurf = pygame.Surface( surf.get_size(), pygame.SRCALPHA,32 )
    alphasurf.fill((R,G,B,alpha))
    alphasurf.blit(surf,(0,0),surf.get_rect(),mode)
    return alphasurf 

def bounce(value,direction,bouncing=True,valuemin=0,valuemax=255):
    # boucing a value like alpha or color between valuemin and valuemax
    # when bouncing, direction(usually -1 or 1) is inverted when reaching valuemin or max
    value += direction # increase or decrease value by direction
    if value <= valuemin:
        value = valuemin
        if bouncing: direction *= -1
    elif value >=valuemax:
        value = valuemax
        if bouncing: direction *= -1
    return value, direction

def write(msg = 'pygame is cool', size=24, color = white):
    textfont = pygame.font.SysFont('None',size)
    textsurf = textfont.render(msg,True,color).convert_alpha()
    return textsurf
def alphademo(width=800,height=600):
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    background = pygame.Surface( screen.get_size() ).convert()
    #background.fill(white)
    venus = pygame.image.load(os.path.join("data","800px-La_naissance_de_Venus.jpg")).convert()
    # transform venus and blit on background in one go
    pygame.transform.scale(venus,(width,height),background)
    # -------- png image with convert_alpha() ------------
    # .png and .gif graphics can have transparency.
    pngMonster = pygame.image.load(os.path.join("data", "colormonster.png")).convert_alpha()
    pngMonster0 = pngMonster.copy()
    pngMonster3 = pngMonster.copy() # for per-pixel alpha
    # --------- jpg image ---------------------------------
    # using .convert() at an .jpg is the same as a .jpg
    # => no transparency
    jpgMonster = pygame.image.load(os.path.join("data","colormonster.jpg")).convert()
    jpgMonster0 = jpgMonster.copy()
    jpgMonster1 = jpgMonster.copy() # to demonstrate colorkey
    jpgMonster1.set_colorkey(white) # make white transparent
    jpgMonster1.convert_alpha()
    jpgMonster2 = jpgMonster.copy() # for surface alpha
    jpgMonster3 = jpgMonster.copy() # for per-pixel alpha
    #--------- text surfaces -------------------------------
    png0text = write('png has alpha')
    png3text = write('png with pixel-alpha')
    jpg0text = write('jpg no alpha')
    jpg1text = write('jpg with colorkey')
    jpg2text = write('jpg with surface alpha')
    jpg3text = write('jpg with pixel-alpha')
    # -------- for bitmap-alpha ----------------------------
    alpha = 128
    direction = 1 # change of alpha
    # -------- for per-pixel alpha -------------------------
    R,G,B,A = 255,255,255,255
    modeNr = 7
    # index 7, int-value 8, name ='BLEND_RGB_MULT', usage = pygame.BLEND_RGB_MULT
    paper = pygame.Surface( (400,100) ) # background for instructions
    # paper.fill(black)
    paper.set_alpha(128) # half transparent 

    modelist = [ 'BLEND_ADD', 'BLEND_SUB', 'BLEND_MULT', 'BLEND_MIN', 'BLEND_MAX',
                 'BLEND_RGBA_ADD', 'BLEND_RGBA_SUB', 'BLEND_RGBA_MULT', 'BLEND_RGBA_MIN', 'BLEND_RGBA_MAX' ]

    # ------ mainloop -------
    clock = pygame.time.Clock()
    mainloop = True
    effects = False
    while mainloop:
        clock.tick(30)
        screen.blit(background,(0,0)) # draw background every frame
        pygame.display.set_caption("insert/del=red:%i, home/end=green:%i, pgup/pgdwn=blue:%i, +/-=pixalpha:%i press ESC"
               % ( R, G, B, A))
        # event handler
        for e in pygame.event.get():
            if e.type == pygame.QUIT or \
               e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                mainloop = False
            if e.type == pygame.KEYDOWN: # press and release key
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    # modeNr += 1
                    # if modeNr > 9: modeNr = 0 # cycle throught 0~9
                    modeNr = ( modeNr + 1) % len(modelist) # by yipyip

        mode = pygame.constants.__dict__[modelist[modeNr]]
        # ---------- keyb is pressed ? -------------------
        dR,dG,dB,dA = 0,0,0,0 # set changin to 0 for Red,Green,Blue,pixel-Alpha
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_PAGEUP]:        dB = +1      # blue Up
        if pressedkeys[pygame.K_PAGEDOWN]:      dB = -1      # blue Down
        if pressedkeys[pygame.K_HOME]:          dG = +1      # Green Up
        if pressedkeys[pygame.K_END]:           dG = -1      # Green Down
        if pressedkeys[pygame.K_INSERT]:        dR = +1      # Red Up
        if pressedkeys[pygame.K_DELETE]:        dR = -1      # Red Down
        if pressedkeys[pygame.K_KP_PLUS]:       dA = +1      # Alpah Up
        if pressedkeys[pygame.K_KP_MINUS]:      dA = -1      # Alpah Down
        # --------- change color and alpha values -----------
        alpha,direction = bounce(alpha, direction) # change alpah
        R,dR = bounce(R,dR,False) # red for per-pixel
        G,dG = bounce(G,dG,False) # green for per-pixel
        B,dB = bounce(B,dB,False) # blue for per-pixel
        A,dA = bounce(A,dA,False) # alpah for per-pixel

        # --------- blit jpgMonster0 as it is, no alpha at all ----------
        screen.blit(jpgMonster0,(0,300))
        screen.blit(jpg0text,(0,550))
        # --------- blit jpgMonster1 with the colorkey set to white -------
        screen.blit(jpgMonster1,(200,300))
        screen.blit(jpg1text,(200,550))
        # --------- blit jpgMonster2 with alpha for whole surface ---------
        jpgMonster2.set_alpha(alpha) # alpha for whole surface
        screen.blit(jpgMonster2,(400,300))
        screen.blit(jpg2text,(400,550))
        screen.blit( write('surface-alpha: %i' %alpha), (400,570) )
        # --------- blit jpgMonster3 with per-pixel alpha -----------------
        tmp = get_alpha_surface( jpgMonster3, A,R,G,B, mode) # get current alpha
        screen.blit(tmp,(600,300))
        screen.blit(jpg3text,(600,550))
        # --------- blit pngMonster0 as it is, with transparency from image 
        screen.blit( pngMonster0, (0,0) )
        screen.blit( png0text,(0,200))
        # -------- blit pngMonster1 with colorkey set to black -----------
        # *** png already has alpha, does not need color key ***
        # ------- blit pngMonster2 with alpha for whole surface ----------
        # *** surface-alpha does not work if surface(png) already has alpah ***
        # ------- blit pngMoster3 with per-pixel alpha --------------------
        tmp = get_alpha_surface(pngMonster3, A, R, G, B, mode) # get current alpha
        screen.blit(tmp, (600,10))
        screen.blit(png3text, (600,200))
        # ---- instructions ----
        screen.blit(paper, (188,150)) #  semi-transparent background for instructions
        screen.blit(write("press [INS] / [DEL] to change red value: %i" % R,24, (255,255,255)),(190,150))
        screen.blit(write("press [HOME] / [END] to change green value: %i" % G),(190,170))
        screen.blit(write("press [PgUp] / [PgDwn] to chgange blue value: %i"% B), (190, 190))
        screen.blit(write("press [Enter] for mode: %i (%s)" % (mode, modelist[modeNr])), (190,230))
        screen.blit(write("press [+] / [-] (Keypad) to chgange alpha value: %i"% A), (190, 210))
        # ------ next frame --------
        pygame.display.flip()       # flip the screen 30 times a second
        
if __name__ == "__main__":
    alphademo()
