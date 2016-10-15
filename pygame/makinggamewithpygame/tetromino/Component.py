import pygame, sys, random, time
import pygame,sys,random
from constants2 import *
from pygame.locals import *


def converToPixelPos(boardpos):
    return (boardpos.x*boxsize,boardpos.y*boxsize)

def converTo2D(index,width):
    return BoardPos(index % width, index // width)

def converTo1D(boardpos,width):
    return boardpos.x + width*boardpos.y

def drawBox(surface,index,char):
    boardpos = converTo2D(index,boardwidth)
    pixelX,pixelY = converToPixelPos(boardpos)
    # draw box border
    outerrect = pixelX-1,pixelY-1,boxsize+2,boxsize+2
    pygame.draw.rect(surface,gridcolor,outerrect)
    # draw inner box
    rect = pixelX,pixelY,boxsize,boxsize
    pygame.draw.rect(surface,boardbgcolor,rect)
    if char == blank: return
    # draw non-blank box
    color = char
    rect = pixelX,pixelY,boxsize,boxsize
    pygame.draw.rect(surface,color,rect)
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
    shapes = ['S','J','I','L','Z','O','T'] #shapes = ['S','Z'] * 2 #shapes = ['S','Z','I','O'] 
    def __init__(self):
        self.shape = random.choice(self.shapes) #print self.shape
        self.width,self.height = 5,5
        self.pieces = pieces[self.shape] #print 'pieces: ',self.pieces
        self.piece = random.choice(self.pieces) #print 'piece : ',self.piece
        self.startpos = BoardPos(3,-2)
        self.color = random.choice(colors)
    def rotate(self):
        idx = self.pieces.index(self.piece)
        rotate(self.pieces)
        self.piece = self.pieces[idx]

    def converToBoardPos(self,index):
        return self.startpos + converTo2D(index,self.width)

    def draw(self,surface):
        for index,char in enumerate(self.piece):
            #print index,char
            self.drawBox(surface,index,char)

    def drawBox(self,surface,index,char):
        if char == blank:
            color = boardbgcolor 
            #print color
        else:
            color = self.color #blue
        boardpos = self.converToBoardPos(index)
        pixelX,pixelY = converToPixelPos(boardpos)
        rect = pixelX,pixelY,boxsize,boxsize
        pygame.draw.rect(surface,gridcolor2,rect)
        innerrect = pixelX+1,pixelY+1,boxsize-2,boxsize-2
        pygame.draw.rect(surface,color,innerrect)


class Board:
    def __init__(self):
        self.width,self.height = boardwidth, boardheight
        self.board = self.generateNewBoard()
        self.resolution = self.width*boxsize, self.height*boxsize
        self.surface = pygame.Surface(self.resolution)
        self.rect = self.surface.get_rect()
        self.rect.topleft = width/3,30
        self.fallingpiece = self.generateNewPiece()
        self.nextpiece = self.generateNewPiece()
        #self.board[30] = '#'

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

    def addToBoard(self,piece):
        for index,char in enumerate(piece.piece):
            if char == blank: continue
            # char = '#'
            boardpos = piece.converToBoardPos(index)
            self.board[self.converToIndex(boardpos)] = piece.color

    def movePiece(self,move=down):
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
        import copy
        piece = copy.deepcopy(piece)
        if move == left:  piece.startpos.x += -1 
        if move == right: piece.startpos.x += +1 
        if move == down:  piece.startpos.y += +1 
        if move == up:    piece.rotate()
        for index,char in enumerate(piece.piece):
            boardpos = piece.converToBoardPos(index) 
            isAboveBoard = boardpos.y < 0
            if isAboveBoard or char == blank: continue
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

    def printboard(self):
        for index, char in enumerate(self.board):
            if index != 0 and index % self.width == 0:
                print
            print index,char,
        print

    def draw(self,displaysurf):
        print self.fallingpiece
        self.drawBorder(displaysurf)
        self.drawBoard()
        self.fallingpiece.draw(self.surface)
        displaysurf.blit(self.surface,self.rect)

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
            drawBox(self.surface,index,char)
            #boardpos = converTo2D(index,self.width)




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

