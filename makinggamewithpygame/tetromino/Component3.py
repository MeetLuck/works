from constants3 import *

def converToPixelPos(boardpos):
    return (boardpos.x*boxsize,boardpos.y*boxsize)

def converTo2D(index,width):
    return BoardPos(index % width, index // width)

def converTo1D(boardpos,width):
    return boardpos.x + width*boardpos.y

def drawBox(surface,index,bgcolor,color):
    boardpos = converTo2D(index,boardwidth)
    pixelX,pixelY = converToPixelPos(boardpos)
    rect = pixelX,pixelY,boxsize,boxsize
    pygame.draw.rect(surface,boardbgcolor,rect)
    if color == blank: return
    # draw non-blank box
    darkcolor = converToDarkColor(color)
    shadowrect = pixelX+1,pixelY+1,boxsize-1,boxsize-1
    pygame.draw.rect(surface,darkcolor,shadowrect)
    # draw inner box
    outerrect = pixelX+1,pixelY+1,boxsize-4,boxsize-4
    pygame.draw.rect(surface,color,outerrect)
#   innerrect = pixelX-1,pixelY-1,boxsize-1,boxsize-1
#   pygame.draw.rect(surface,color,innerrect)

def isOnBoard(boardpos):
    return 0 <= boardpos.x < boardwidth and boardpos.y < boardheight

def rotate(lst):
    return lst.insert(0,lst.pop())

class BoardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __add__(self,other):
        return BoardPos(self.x + other.x, self.y+other.y)

class Piece:
    shapes = [tetrisS,tetrisZ,tetrisI,tetrisO,tetrisJ,tetrisL,tetrisT]
    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.width,self.height = 5,5
        self.pieces = [rotate90(self.shape) for i in range(4) ]
        self.piece = random.choice(self.pieces) #print 'piece : ',self.piece
        self.startpos = BoardPos(3,-2)
        self.color = random.choice(colors)
    def rotate(self):
        #idx = self.pieces.index(self.piece)
        #rotate(self.pieces)
        self.piece = rotate90(self.piece)
    def converToBoardPos(self,x,y):
        return self.startpos + BoardPos(x,y)

    def draw(self,surface):
        for x in range(self.width):
            for y in range(self.height):
                boardpos = self.converToBoardPos(x,y)
                char = self.piece[x][y]
                self.drawBox(surface,boardpos,char)

    def drawBox(self,surface,boardpos,char):
        if char == blank:
            color = boardbgcolor 
            #print color
        else:
            color = self.color #blue
        pixelX,pixelY = converToPixelPos(boardpos)
        rect = pixelX,pixelY,boxsize,boxsize
        pygame.draw.rect(surface,gridcolor2,rect)
        innerrect = pixelX+1,pixelY+1,boxsize-2,boxsize-2
        pygame.draw.rect(surface,color,innerrect)


class Board:
    def __init__(self,level=1):
        self.level = level
        self.setSpeed()
        self.width,self.height = boardwidth, boardheight
        self.board = self.generateNewBoard()
        self.resolution = self.width*boxsize, self.height*boxsize
        self.surface = pygame.Surface(self.resolution)
        self.rect = self.surface.get_rect()
        self.rect.topleft = screenwidth-2*xmargin,topmargin-20
        self.fallingpiece = self.generateNewPiece()
        self.nextpiece = self.generateNewPiece()
        self.completelines = 0
        self.maxlines = 1 + 1 * (self.level-1)
        #self.maxlines = 19 + 10 * self.level
        #self.board[30] = '#'
    def setSpeed(self):
        tp = 1.0/fps
        if 1<= self.level <= 5:
            speedup = self.level + 4
        elif 6<= self.level <= 10:
            speedup = self.level + 7 
        elif 11<= self.level <= 15:
            speedup = self.level + 10 
        else:
            sppedup = 25
        self.fallfreq = (31 - speedup) * tp

    def generateNewBoard(self):
        return [blank] * self.width * self.height
    def generateNewPiece(self):
        newpiece = Piece()
        return newpiece
    def converToBoardPos(self,index):
        return converTo2D(index,self.width)
    def converToIndex(self,boardpos):
        return converTo1D(boardpos,self.width)

    def generateNextPieces(self):
        self.fallingpiece = self.nextpiece
        self.nextpiece = self.generateNewPiece()
        p = self.fallingpiece
        for y in range(p.height): # row
            for x in range(p.width): # col
                print p.piece[x][y],
            print 

    def addToBoard(self,piece):
        for x in range(piece.width):
            for y in range(piece.height):
                char = piece.piece[x][y]
                if char == blank: continue
                # char = '#'
                boardpos = piece.converToBoardPos(x,y)
                self.board[self.converToIndex(boardpos)] = piece.color

    def movePiece(self,move):
        if move == left:
            self.fallingpiece.startpos.x += -1
        elif move == right:
            self.fallingpiece.startpos.x += +1
        elif move == down:
            self.fallingpiece.startpos.y += +1
        else:
            print 'not allowed move'

    def isValidPosition(self,piece,move):
        # Return True if the piece is within the board and not colliding
        piece = copy.deepcopy(piece)
        if move == left:  piece.startpos.x += -1 
        if move == right: piece.startpos.x += +1 
        if move == down:  piece.startpos.y += +1 
        if move == up:    piece.rotate()
        for x in range(piece.width):
            for y in range(piece.height):
                boardpos = piece.converToBoardPos(x,y) 
                isAboveBoard = boardpos.y < 0
                if isAboveBoard or piece.piece[x][y] == blank: continue
                # char = '#'
                boardindex = self.converToIndex(boardpos) #converTo1D(boardpos,boardwidth)
                if not isOnBoard(boardpos):
                    return False
                if self.board[boardindex] != blank:
                    return False
        return True
    def isCompleteLine(self,boardY):
        for x in range(0,boardwidth):
            boardpos = BoardPos(x,boardY)
            index = converTo1D(boardpos,self.width)
            if self.board[index] == blank:
                return
        self.completelines += 1
        return True

    def removeCompleteLines(self):
        # Remove any completed lines on the board, move everything above them down,
        # and return the number of complete lines.
        numLinesRemoved = 0
        boardY = self.height - 1 # start y at the bottom of the board
        while boardY >= 0:
            if self.isCompleteLine(boardY):
                # Remove the line and pull boxes down by one line.
                for x in range(boardwidth):
                    boardpos = BoardPos(0,boardY)
                    index = converTo1D(boardpos,self.width)
                    del self.board[index]
                # Set very top line to blank.
                for x in range(self.width):
                    self.board.insert(0,blank)
                numLinesRemoved += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                boardY -= 1 # move on to check next row up
        return numLinesRemoved
    def completeLevel(self):
        if self.completelines >= self.maxlines:
            return True
        return False

    def printboard(self):
        for index, char in enumerate(self.board):
            if index != 0 and index % self.width == 0:
                print
            print index,char,
        print

    def draw(self,displaysurf):
        #print self.fallingpiece
        self.drawBorder(displaysurf)
        self.drawBoard()
        self.fallingpiece.draw(self.surface)
        displaysurf.blit(self.surface,self.rect)
        self.drawLevel(displaysurf)
        self.drawNextPiece(displaysurf)
        self.drawStatus(displaysurf)

    def drawBorder(self,displaysurf):
        #border_width,border_height = self.width*boxsize+20, self.height*boxsize + 20
        w,h = self.resolution
        x,y = self.rect.topleft
        border_rect = x-5,y-5, w+10,h+10
        pygame.draw.rect(displaysurf,bordercolor,border_rect)
        border_rect = x-4,y-4, w+8,h+8
        pygame.draw.rect(displaysurf,bordercolor2,border_rect)


    def drawBoard(self): #,surface):
        for index,char in enumerate(self.board):
            drawBox(self.surface,index,gridcolor,char)
            #boardpos = converTo2D(index,self.width)
    def drawStatus(self,displaysurf):
        starty = 150
        lightcolor = 'orange4'
        color = 'orange'
        #  completed : 
        textsurf,textrect = getText(text='completed : ', fontsize=18, color=lightcolor)
        textrect.topleft = screenwidth - 150, starty
        displaysurf.blit(textsurf,textrect)
        # completed : number
        textsurf,textrect = getText(text='%d' %self.completelines, fontsize=18, color=color)
        textrect.topleft = screenwidth - 40, starty
        displaysurf.blit(textsurf,textrect)

        # left : 
        textsurf,textrect = getText(text='left : ',fontsize=18, color=lightcolor)
        textrect.topleft = screenwidth - 150, starty+25
        displaysurf.blit(textsurf,textrect)
        # left : number 
        textsurf,textrect = getText(text='%d' %(self.maxlines-self.completelines), fontsize=18, color=color)
        textrect.topleft = screenwidth - 100, starty+25
        displaysurf.blit(textsurf,textrect)

    def drawLevel(self,displaysurf):
        # Level : 
        textsurf,textrect = getText(text='Level : %d' %self.level, fontsize=35, color='orange3')
        textrect.topleft = screenwidth - 160, 80 
        displaysurf.blit(textsurf,textrect)


    def drawNextPiece(self,displaysurf):
        # next : 
        textsurf,textrect = getText(text='Next : ', fontsize=18, color='orange')
        textrect.topleft = screenwidth - 150, 220 
        displaysurf.blit(textsurf,textrect)
        # draw the "next" piece
        w = self.nextpiece.width * boxsize + 2 
        h = self.nextpiece.height * boxsize + 2 
        nextsurf = pygame.Surface((w,h))
        nextrect = nextsurf.get_rect()
        nextrect.topleft = screenwidth-150, 250 
        #nextsurf.fill(white)
        tmp_piece = copy.deepcopy(self.nextpiece)
        tmp_piece.startpos = BoardPos(0,0)
        tmp_piece.draw(nextsurf)
        displaysurf.blit(nextsurf,nextrect)
        #drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

def getText(text,font='freesansbold.ttf',fontsize=20,color='white',bgcolor='black'):
    fontobj = pygame.font.Font(font,fontsize)
    textsurf = fontobj.render(text,True,pygame.Color(color),pygame.Color(bgcolor))
    textrect = textsurf.get_rect()
    return textsurf,textrect 

def converToDarkColor(color):
    r,g,b,a = color
    lightcolor = r*0.9,g*0.9,b*0.9,a
    return lightcolor


if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((width,height))
    mb = Board()
    surface.fill(bgcolor)
    print 'start drawing...'
    mb.generateNewPiece()
    mb.draw(surface)
    mb.drawPiece()
    pygame.display.update()
    pygame.time.wait(5999)

