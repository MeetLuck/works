from constants4 import *

def converToPixelPos(boardpos):
    return (boardpos.x*boxsize,boardpos.y*boxsize)
def converTo2D(index,width):
    return BoardPos(index % width, index // width)
def converTo1D(boardpos,width):
    return boardpos.x + width*boardpos.y
def getValue(list2D,x,y):
    'list of lists : [ row1,row2,...,rowN]'
    return list2D[y][x]
def isOnBoard(boardpos):
    return 0 <= boardpos.x < boardwidth and boardpos.y < boardheight
#def rotate(lst):
#    return lst.insert(0,lst.pop())

def drawBox(surface,boardpos,bgcolor,gridcolor,color):
    pixelX,pixelY = converToPixelPos(boardpos)
    #------ draw blank box ---------------------
    rect = pixelX,pixelY,boxsize,boxsize
    pygame.draw.rect(surface,gridcolor,rect)
    rect = pixelX+1,pixelY+1,boxsize-1,boxsize-1
    pygame.draw.rect(surface,bgcolor,rect)
    if color == blank: return
    #----- draw non-blank box ------------------
    # draw shadow box
    darkcolor = getDarkColor(color,90)
    shadowrect = pixelX+1,pixelY+1,boxsize-1,boxsize-1
    pygame.draw.rect(surface,darkcolor,shadowrect)
    # draw inner box
    outerrect = pixelX+1,pixelY+1,boxsize-4,boxsize-4
    pygame.draw.rect(surface,color,outerrect)

class BoardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __add__(self,other):
        return BoardPos(self.x + other.x, self.y+other.y)

class Piece:
    def __init__(self):
        self.piece = self.makePiece()
        self.startpos = BoardPos(3,-2)
        self.color = random.choice(colors)
        self.width, self.height = len(self.piece[0]), len(self.piece)
    def makePiece(self):
        shapes = [tetrisS,tetrisZ,tetrisI,tetrisO,tetrisJ,tetrisL,tetrisT]
        shape = random.choice(shapes)
        pieces = []
        for i in range(4):
            shape = rotate90(shape)
            pieces.append( shape[:] )
        piece = random.choice(pieces)
        #------- print tetris piece ---------
        for piece in pieces:
            for row in piece:
                print ''.join(row)
        return piece
    def rotate(self):
        self.piece = rotate90(self.piece)
    def converToBoardPos(self,x,y):
        return self.startpos + BoardPos(x,y)
    def getValue(self,x,y):
        return getValue(self.piece,x,y)
    def draw(self,surface):
        for x in range(self.width):      # col
            for y in range(self.height): # row
                boardpos = self.converToBoardPos(x,y)
                char = self.getValue(x,y) #[y][x]
                if char == blank:
                    bx,by = converToPixelPos(boardpos)
                    pygame.draw.line(surface,gridcolor2,[bx,by],[bx+boxsize,by],1)
                    pygame.draw.line(surface,gridcolor2,[bx,by],[bx,by+boxsize],1)
                else:
                    color = self.color 
                    drawBox(surface,boardpos,bgcolor,gridcolor2,color)
                #drawBox(surface,boardpos,bgcolor,gridcolor2,char)

class Board:
    def __init__(self,level=1):
        self.level = level
        self.setSpeed()
        self.width,self.height = boardwidth, boardheight
        self.board = self.generateNewBoard()
        self.resolution = self.width*boxsize, self.height*boxsize
        self.surface = pygame.Surface(self.resolution)
        #self.surface.convert_alpha()
        self.rect = self.surface.get_rect()
        #self.rect.topleft = screenwidth-2*xmargin,topmargin-20
        self.rect.center = screenwidth/2, screenheight/2
        self.fallingpiece = self.generateNewPiece()
        self.nextpiece = self.generateNewPiece()
        self.completelines = 0
        self.maxlines = 5 + 3 * (self.level-1)
        #self.maxlines = 19 + 10 * self.level
        #self.board[30] = '#'
    def setSpeed(self):
        tp = 1.0/fps
        if self.level in range(1,5) : # 1~4
            speedup = self.level + 4
        elif self.level in range(5,10): # 5~9
            speedup = self.level + 7 
        elif self.level in range(10,15): # 10 ~ 14
            speedup = self.level + 10 
        else: # 15 ~
            sppedup = 25
        self.fallfreq = (31 - speedup) * tp

    def generateNewBoard(self):
            return [ [blank]*self.width for row in range(self.height) ]
    def generateNewPiece(self):
        return Piece()
    def converToBoardPos(self,index):
        return converTo2D(index,self.width)
    def converToIndex(self,boardpos):
        return converTo1D(boardpos,self.width)
    def getValue(self,x,y):
        return getValue(self.board,x,y)
    def setValue(self,boardpos,value):
        try:
            self.board[boardpos.y][boardpos.x] = value 
        except:
            print boardpos
            print boardpos.x,boardpos.y
    def generateNextPieces(self):
        self.fallingpiece = self.nextpiece
        self.nextpiece = self.generateNewPiece()
    def addToBoard(self,piece):
        for x in range(piece.width):
            for y in range(piece.height):
                char =  piece.getValue(x,y) # char = piece.piece[y][x]
                if char == blank: continue
                # char = '#'
                boardpos = piece.converToBoardPos(x,y)
                self.setValue(boardpos,piece.color)
                # self.board[self.converToIndex(boardpos)] = piece.color

    def movePiece(self,moveX=0,moveY=0):
        assert moveY >= 0, 'not allowed move'
        self.fallingpiece.startpos.x += moveX
        self.fallingpiece.startpos.y += moveY

    def isValidPosition(self,piece,moveX=0,moveY=0):
        # Return True if the piece is within the board and not colliding
        cpiece = copy.deepcopy(piece)
        cpiece.startpos.x += moveX
        cpiece.startpos.y += moveY
        if (moveX,moveY) == (0,-1): cpiece.rotate()

        for x in range(cpiece.width):
            for y in range(cpiece.height): # height
                boardpos = cpiece.converToBoardPos(x,y) 
                isAboveBoard = boardpos.y < 0
                if isAboveBoard or cpiece.getValue(x,y) == blank: continue
                # not blank box,char = '#'
                if not isOnBoard(boardpos):
                    return False
                if self.getValue(boardpos.x,boardpos.y) != blank:
                    return False
        return True

    def isCompleteLine(self,boardY):
        for x in range(0,boardwidth):
            if self.getValue(x,boardY) == blank:
                return
        self.completelines += 1
        #pygame.mixer.init()
        completesound = pygame.mixer.Sound('blip2.wav')
        completesound.play()
        return True

    def removeCompleteLines(self):
        # Remove any completed lines on the board, move everything above them down,
        # and return the number of complete lines.
        numLinesRemoved = 0
        boardY = self.height - 1 # start y at the bottom of the board
        while boardY >= 0:
            if self.isCompleteLine(boardY):
                del self.board[boardY] # Remove the line and pull boxes down by one line.
                self.board.insert(0, [blank]*self.width) # Set very top line to blank.
                numLinesRemoved += 1
            else:
                boardY -= 1 # move on to check next row up
        return numLinesRemoved

    def completeLevel(self):
        if self.completelines >= self.maxlines:
            return True
        return False

    def printboard(self):
        for row in self.board:
            print ''.join(row)

    def draw(self,displaysurf,starttime):
        #print self.fallingpiece
        self.drawBorder(displaysurf)
        self.drawBoard()
        self.fallingpiece.draw(self.surface)
        displaysurf.blit(self.surface,self.rect)
        self.drawNextPiece(displaysurf)
        self.drawStatus(displaysurf,starttime)

    def drawBorder(self,displaysurf):
        #border_width,border_height = self.width*boxsize+20, self.height*boxsize + 20
        w,h = self.resolution
        x,y = self.rect.topleft
        border_rect = x-3,y-3, w+6,h+6
        pygame.draw.rect(displaysurf,bordercolor1,border_rect)
        border_rect = x-2,y-2, w+4,h+4
        pygame.draw.rect(displaysurf,bordercolor2,border_rect)


    def drawBoard(self): #,surface):
        for x in range(self.width):
            for y in range(self.height):
                char = self.getValue(x,y)
                boardpos = BoardPos(x,y)
                drawBox(self.surface,boardpos,bgcolor,gridcolor1,char)
    def drawStatus(self,displaysurf,starttime):
        starty,stepy = 120,25
        titlecolor = getDarkColor('darkgreen',150)
        lightcolor = getDarkColor(titlecolor,90)
        numbercolor = getDarkColor(lightcolor,150)
        # Level : 
        textsurf,textrect = getTextObj(text='LEVEL  %d' %self.level, fontsize=35, color=titlecolor)
        textrect.topleft = screenwidth - 200, 80
        displaysurf.blit(textsurf,textrect)
        # elasped :
        elapsed = time.time() - starttime 
        m,s = divmod(elapsed,60)
        elapsed = '{} : {}'.format(int(m),int(s))
        textsurf,textrect = getTextObj(text = 'elapsed  ', fontsize=18, color=titlecolor)
        textrect.topleft = screenwidth - 200, starty + stepy 
        displaysurf.blit(textsurf,textrect)
        textsurf,textrect = getTextObj(text = elapsed, fontsize=18, color=numbercolor)
        textrect.topleft = screenwidth - 200+90, starty + stepy 
        displaysurf.blit(textsurf,textrect)

        #  completed : 
        textsurf,textrect = getTextObj(text='completed : ', fontsize=18, color=lightcolor)
        textrect.topleft = screenwidth - 200, starty + 2*stepy
        displaysurf.blit(textsurf,textrect)
        # completed : number
        textsurf,textrect = getTextObj(text='%d' %self.completelines, fontsize=18, color=numbercolor)
        textrect.topleft = screenwidth - 80, starty + 2*stepy
        displaysurf.blit(textsurf,textrect)

        # left : 
        textsurf,textrect = getTextObj(text='left : ',fontsize=18, color=lightcolor)
        textrect.topleft = screenwidth - 200, starty + 3*stepy
        displaysurf.blit(textsurf,textrect)
        # left : number 
        textsurf,textrect = getTextObj(text='%d' %(self.maxlines-self.completelines), fontsize=18, color=numbercolor)
        textrect.topleft = screenwidth - 150, starty + 3*stepy
        displaysurf.blit(textsurf,textrect)

    def drawNextPiece(self,displaysurf):
        y = 250
        # next : 
        textsurf,textrect = getTextObj(text='Next : ', fontsize=18, color='darkgreen')
        textrect.topleft = screenwidth - 200, y 
        displaysurf.blit(textsurf,textrect)
        # draw the "next" piece
        w = self.nextpiece.width * boxsize + 2 
        h = self.nextpiece.height * boxsize + 2 
        nextsurf = pygame.Surface((w,h))
        nextrect = nextsurf.get_rect()
        nextrect.topleft = screenwidth-200, y+20 
        nextsurf.fill(bgcolor)
        tmp_piece = copy.deepcopy(self.nextpiece)
        tmp_piece.startpos = BoardPos(0,0)
        tmp_piece.draw(nextsurf)
        displaysurf.blit(nextsurf,nextrect)
        #drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

def getTextObj(text,font='freesansbold.ttf',fontsize=20,color='white'):#,bgcolor='black'):
    if type(color) is str:
        color = pygame.Color(color)
    fontobj = pygame.font.Font(font,fontsize)
    textsurf = fontobj.render(text,True,color) #,pygame.Color(bgcolor))
    return textsurf,textsurf.get_rect()

def getDarkColor(color,percent):
    if type(color) is str: color = pygame.Color(color)
    r,g,b,a = color
    darkcolor = r*percent/100.0,g*percent/100.0,b*percent/100,a
    return darkcolor


if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((screenwidth,screenheight))
    mb = Board()
    surface.fill(bgcolor)
    print 'start drawing...'
    mb.generateNewPiece()
    mb.draw(surface)
#   mb.drawPiece()
    pygame.display.update()
    pygame.time.wait(5999)

