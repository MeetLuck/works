''' 004 alphademo pretty.py
colorkey and alpha-value
'''
import pygame,os,itertools

white = pygame.Color('white')
yellow = pygame.Color('yellow')
BLENDMODES = [ (pygame.BLEND_ADD,'ADD'), (pygame.BLEND_SUB,'SUB'), (pygame.BLEND_MULT,'MULT'),
               (pygame.BLEND_MIN,'MIN'), (pygame.BLEND_MAX,'MAX'),
               (pygame.BLEND_RGBA_ADD,'RGBA ADD'), (pygame.BLEND_RGBA_SUB,'RGBA SUB'), (pygame.BLEND_RGBA_MULT,'RGBA MULT'),
               (pygame.BLEND_RGBA_MIN,'RGBA MIN'), (pygame.BLEND_RGBA_MAX,'RGBA MAX')  ]

def load_pic(name,path='data'):
    return pygame.image.load(os.path.join(path,name))

def check(x,minval=0,maxval=255):
    return min(maxval,max(minval,x))

def get_alpha_surface(surface,rgba=(128,128,128,128),mode=pygame.BLEND_RGBA_ADD):
    # return a copy of surface object with user-defined value for R,G,B,and A
    newsurf = pygame.Surface(surface.get_size(),pygame.SRCALPHA|pygame.HWSURFACE)
    newsurf.fill(rgba)
    newsurf.blit(surface,(0,0),surface.get_rect(),mode)
    return newsurf

class AlphaDemo(object):
    def __init__(self,width=900,height=600,fontsize=14):
        pygame.init()
        self.screen = pygame.display.set_mode( (width,height),pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.SysFont('mono',fontsize,bold=True)
        self.clock = pygame.time.Clock()
        # self.background.fill(white)
        venus = load_pic("800px-La_naissance_de_Venus.jpg").convert()
        # transform venus and blit 
        pygame.transform.scale(venus,(width,height),self.background)
        # .png and .gif graphics can have transparency, use convert_alpha()
        self.png_monster = load_pic("colormonster.png").convert_alpha()
        # jpg image, no transparency!
        self.jpg_monster = load_pic("colormonster.jpg").convert()
        # per-pixel RGBA
        self.pp_rgba = (255,255,255,128)
        alpha_up = range(0,256,4)
        alpha_down = alpha_up[-1::-1]
        self.glob_alphas = itertools.cycle(alpha_up+alpha_down)
        #print self.glob_alphas
        self.step = 4
        self.mode_nr = 5

    def run(self): # mainloop
        mainloop = True
        while mainloop:
            # event handler
            for e in pygame.event.get():
                if e.type == pygame.QUIT or \
                   e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    mainloop = False
            self.action(pygame.key.get_pressed())
            pygame.display.flip()
            # draw background every frame
            self.screen.blit(self.background,(0,0))
            self.clock.tick(20)

    def action(self,pressed_keys):
        R,G,B,A = self.pp_rgba
        if pressed_keys[pygame.K_PAGEUP]:   B += self.step
        if pressed_keys[pygame.K_PAGEDOWN]: B -= self.step
        if pressed_keys[pygame.K_HOME]:     G += self.step
        if pressed_keys[pygame.K_END]:      G -= self.step
        if pressed_keys[pygame.K_INSERT]:   R += self.step
        if pressed_keys[pygame.K_DELETE]:   R -= self.step
        if pressed_keys[pygame.K_KP_PLUS]:  A += self.step
        if pressed_keys[pygame.K_KP_MINUS]: A -= self.step
        if pressed_keys[pygame.K_RETURN]:
            self.mode_nr = (self.mode_nr + 1) % len(BLENDMODES)
        mode,mode_text = BLENDMODES[self.mode_nr]
        print mode, mode_text
        self.pp_rgba = map( check, (R,G,B,A) )
        glob_alpha = self.glob_alphas.next()
        self.show_surface(self.png_monster, 'png',0,0,200,180, glob_alpha, self.pp_rgba,mode)
        self.show_surface(self.jpg_monster, 'jpg',0,300,200,180, glob_alpha, self.pp_rgba,mode)
        text = "ins/del=red>%d  home/end=green>%d  pgup/pgdwn=blue>%d  "\
                "+/-=ppalpha>%d  " % tuple(self.pp_rgba)
        pygame.display.set_caption('%s mode>%s' %(text,mode_text))

    def show_surface(self,surf,pictype,x,y,x_delta,height,glob_alpha,pp_rgba,mode):
        yh = y + height
        # pure surface
        self.screen.blit(surf,(x,y))
        self.write(x,y+height, '%s pure' %pictype)
        # with colorkey
        ck_surf = surf.copy()
        ck_surf.set_colorkey(white)
        x += x_delta
        self.screen.blit(ck_surf,(x,y))
        self.write(x,yh,'%s alpha>%d' %(pictype,glob_alpha) )
        # with per-pixel alpha
        ppasurf = surf.copy()
        ppasurf = get_alpha_surface(ppasurf,pp_rgba,mode)
        x += x_delta
        self.screen.blit(ppasurf,(x,y))
        self.write(x,yh,'%s, per-pixel-alpha' %pictype)
    def write(self,x,y,msg,color=yellow):
        self.screen.blit(self.font.render(msg,True,color),(x,y))

if __name__ == '__main__':
    AlphaDemo().run()


            



