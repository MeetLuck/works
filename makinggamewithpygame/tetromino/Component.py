import pygame, sys, random, time
from constants import *
from pygame.locals import *


def converToPixelPos(boardpos):
    return (boardpos.x*boxsize,boardpos.y*boxsize)

def converTo2D(index,width):
    return BoardPos(index % width, index // width)

def converTo1D(boardpos,width):
    return boardpos.x + width*boardpos.y

def drawBox(surface,index,char):
    if char == blank:
        color = boardbgcolor #220,220,220 #bgcolor
    else:
        color = blue
    boardpos = converTo2D(index,boardwidth)
    pixelX,pixelY = converToPixelPos(boardpos)
    rect = pixelX,pixelY,boxsize,boxsize
    pygame.draw.rect(surface,color,rect)

def isOnBoard(boardpos):
    return 0 <= boardpos.x < boardwidth and boardpos.y < boardheight

def isValidPosition(board,piece,move):
    # Return True if the piece is within the board and not colliding
    import copy
    piece = copy.deepcopy(piece)
    if move == left:  piece.startpos.x += -1 
    if move == right: piece.startpos.x += +1 
    if move == down: piece.startpos.y += +1 
    if move == None: return True
    for index,char in enumerate(piece.piece):
        if char == blank: continue
        # char = '#'
        boardpos = piece.converToBoardPos(index) 
        boardindex = converTo1D(boardpos,boardwidth)
        if not isOnBoard(boardpos):
            return False
        if board[boardindex] != blank:
            return False
    return True

class BoardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __add__(self,other):
        return BoardPos(self.x + other.x, self.y+other.y)

class Piece:
    def __init__(self,name):
        self.name = name
        #self.shape = random.choice(pieces)
        print S[0]
        self.width,self.height = 5,5
        self.piece = S[0]
        self.startpos = BoardPos(3,0)
        self.color = random.choice(colors)
    def draw(self,surface):
        for index,char in enumerate(self.piece):
            #print index,char
            self.drawBox(surface,index,char)
    def converToBoardPos(self,index):
        self.boardpos = self.startpos + converTo2D(index,self.width)
        return self.boardpos

    def drawBox(self,surface,index,char):
        if char == blank:
            color = boardbgcolor[0]*2, boardbgcolor[1]*2, boardbgcolor[2]*2 #120,120,120 #bgcolor
            #print color
        else:
            color = self.color #blue
        boardpos = self.converToBoardPos(index)
        pixelX,pixelY = converToPixelPos(boardpos)
        rect = pixelX,pixelY,boxsize,boxsize
        pygame.draw.rect(surface,color,rect)


class Board:
    def __init__(self):
        self.width,self.height = boardwidth, boardheight
        self.board = self.generateNewBoard()
        self.generateNewPiece()
        self.resolution = self.width*boxsize, self.height*boxsize
        self.surface = pygame.Surface(self.resolution)
        self.rect = self.surface.get_rect()
        self.rect.topleft = width/3,30
        self.board[30] = '#'

    def printboard(self):
        for index, char in enumerate(self.board):
            if index != 0 and index % self.width == 0:
                print
            print index,char,
        print

    def draw(self,displaysurf):
        self.drawBoard()
        self.drawPiece()
        displaysurf.blit(self.surface,self.rect)

    def drawBoard(self): #,surface):
        for index,char in enumerate(self.board):
            drawBox(self.surface,index,char)
            boardpos = converTo2D(index,self.width)
            #print self.board[index],
            if boardpos.x % self.width == 0:
                print
        
    def generateNewPiece(self):
        self.fallingpiece = Piece('S')

    def drawPiece(self):
        self.fallingpiece.draw(self.surface)
    def addToBoard(self,piece):
        for index,char in enumerate(piece.piece):
            if char == blank: continue
            # char = '#'
            boardpos = piece.converToBoardPos(index)
            self.board[converTo1D(boardpos,self.width)] = char
    def movePiece(self,move=down):
        if not isValidPosition(self.board,self.fallingpiece,move):
            if move == down:
                self.addToBoard(self.fallingpiece)
                self.generateNewPiece()
            #print 'not valid move',self.fallingpiece.startpos
            return False
        print self.fallingpiece.startpos.x, self.fallingpiece.startpos.y
        if move == left:
            self.fallingpiece.startpos.x += -1
        elif move == right:
            self.fallingpiece.startpos.x += +1
        elif move == down:
            self.fallingpiece.startpos.y += +1
        else: # move down
            return None
    def generateNewBoard(self):
        return [blank] * self.width * self.height





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

