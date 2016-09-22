import pygame, sys, random, time
from constants import *
from pygame.locals import *

class BoardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __add__(self,other):
        return BoardPos(self.x + other.x, self.y+other.y)

class NewPiece:
    def __init__(self,name):
        self.name = name
        #self.shape = random.choice(pieces)
        print S[0]
        self.piece = S[0]
        self.startpos = BoardPos(3,0)
        self.color = random.choice(colors)
    def draw(self,surface):
        for index,char in enumerate(self.piece):
            print index,char
            self.drawBox(surface,index,char)
    def converToBoardPos(self,index):
        self.x,self.y = index % 5, index // 5
        self.boardpos = self.startpos + BoardPos(self.x,self.y)
        return self.boardpos

    def drawBox(self,surface,index,char):
        if char == blank:
            color = boardbgcolor[0]*2, boardbgcolor[1]*2, boardbgcolor[2]*2 #120,120,120 #bgcolor
            print color
        else:
            color = self.color #blue
        boardpos = self.converToBoardPos(index)
        pixelX,pixelY = converToPixelPos(boardpos)
        rect = pixelX,pixelY,boxsize,boxsize
        pygame.draw.rect(surface,color,rect)



def converToPixelPos(boardpos):
    return (boardpos.x*boxsize,boardpos.y*boxsize)

def converTo2D(index):
    return BoardPos(index % boardwidth, index // boardwidth)

def drawBox(surface,index,char):
    if char == blank:
        color = boardbgcolor #220,220,220 #bgcolor
    else:
        color = blue
    boardpos = converTo2D(index)
    pixelX,pixelY = converToPixelPos(boardpos)
    rect = pixelX,pixelY,boxsize,boxsize
    pygame.draw.rect(surface,color,rect)

class Board:
    def __init__(self):
        self.width = boardwidth
        self.height = boardheight
        self.length = self.width * self.height
        self.board = self.generateNewBoard()
        self.resolution = self.width*boxsize, self.height*boxsize
        self.surface = pygame.Surface(self.resolution)
        self.rect = self.surface.get_rect()
        self.rect.topleft = width/3,30
        self.board[30] = '#'

    def draw(self,displaysurf):
        self.drawBoard()
        self.drawPiece()
        displaysurf.blit(self.surface,self.rect)

    def drawBoard(self): #,surface):
        for index,char in enumerate(self.board):
            drawBox(self.surface,index,char)
            boardpos = converTo2D(index)
            print self.board[index],
            if boardpos.x % self.width == 0:
                print
        
    def generateNewPiece(self):
        self.fallingpiece = NewPiece('S')

    def drawPiece(self):
        self.fallingpiece.draw(self.surface)

    def movePiece(self,move=down):
        if move == left:
            self.fallingpiece.startpos.x += -1
        elif move == right:
            self.fallingpiece.startpos.x += +1
        elif move == down:
            self.fallingpiece.startpos.y += +1
        else: # move down
            return
    def generateNewBoard(self):
        return [blank] * self.length

    def isOnBoard(self,boardpos):
        return 0 <= boardpos.x < boardwidth and boardpos.y < boardheight
    def isValidPosition(self):
        # Return True if the piece is within the board and not colliding
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                isAboveBoard = y + piece['y'] + adjY < 0
                if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                    continue
                if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    return False
                if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                    return False
        return True



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

