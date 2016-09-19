import pygame, sys, random, itertools
from pygame.locals import *
from constants import *


def converTo2D(index):
    return boardPos(index%boardwidth, index//boardheight)
def converTo1D(boardpos):
    return boardpos.x + boardwidth * boardpos.y
def converToPixelPos(boardpos):
    boardX,boardY = boardpos.x, boardpos.y
    left = xmargin + (boardX*tilesize) + (boardX-1)
    top  = ymargin + (boardY*tilesize) + (boardY-1)
    return (left,top)

class boardPos:
    def __init__(self,x,y):
        self.x, self.y = x,y
    def __str__(self):
        return 'board(%s,%s)' % (self.x,self.y)

class Tile:
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return 'Tile(%s)' % self.name
    def setBoardPos(self,index):
        self.index = index
        self.boardpos = converTo2D(self.index)
        self.x,self.y = self.boardpos.x, self.boardpos.y
        self.pos = converToPixelPos(self.boardpos)
    def drawTile(self, surface,adjx=0,adjy=0): # draw a tile at board coordinates boardpos
        # optionally a few mouses over (determined by adjx and ajdy)
        basicfont = pygame.font.Font('freesansbold.ttf',basicfontsize)
        x,y = self.pos
        if self.name != None:
            pygame.draw.rect(surface, tilecolor, (x + adjx, y + adjy, tilesize, tilesize))
            textsurf = basicfont.render( str(self.name), True, textcolor)
        else:
            pygame.draw.rect(surface, bgcolor, (x + adjx, y + adjy, tilesize, tilesize))
            textsurf = basicfont.render( str(self.name), True, blankcolor)
        textrect = textsurf.get_rect()
        textrect.center = x + int(tilesize/2) + adjx, y + int(tilesize/2) + adjy
        surface.blit(textsurf, textrect)

class Board:
    def __init__(self,surface):
        self.length = boardwidth*boardheight
        self.startboard = self.getStartingBoard()
        self.board = self.startboard[:]
        self.generateNewPuzzle(surface,numSlides=80)
    def converToBoardPos(self,mouseX,mouseY):
        # from the mouse coordinates, get the board coordinates
        for tile in self.startboard:
            tileRect = pygame.Rect(tile.pos,(tilesize,tilesize))
            if tileRect.collidepoint(mouseX,mouseY):
                return tile.boardpos
        return (None,None)
    def isSolved(self):
        return self.startboard == self.board
    def getBlankTile(self):
        return filter(lambda tile:tile.name == None,self.board)[0]
    def getRandomMove(self,lastMove=None):
        validMoves = [up,down,left,right]
        if lastMove == up or not self.isValidMove(down):
            validMoves.remove(down)   # moved from DOWN
        if lastMove == down or not self.isValidMove(up):
            validMoves.remove(up)     # moved from UP
        if lastMove == left or not self.isValidMove(right):
            validMoves.remove(right)  # moved from RIGHT
        if lastMove == right or not self.isValidMove(left):
            validMoves.remove(left)   # moved from LEFT
        return random.choice(validMoves) # a random move from validMoves
    def getTileAtPos(self,boardpos):
        return self.board[converTo1D(boardpos)] # index = converTo1D(boardpos)
    def getTileAtPosXY(self,boardX,boardY):
        return self.getTileAtPos( boardPos(boardX,boardY) )  #boardpos = boardPos(boardX,boardY)
    def isValidMove(self,move):
        blank = self.getBlankTile()
        return (move == up and blank.y != boardheight-1) or \
               (move == down and blank.y != 0) or \
               (move == left and blank.x != boardwidth-1) or \
               (move == right and blank.x != 0)
    def makeMove(self,move):
        if not self.isValidMove(move): return
        blank = self.getBlankTile()
        if move == up:    tile = self.getTileAtPosXY(blank.x,blank.y+1)
        if move == down:  tile = self.getTileAtPosXY(blank.x,blank.y-1)
        if move == left:  tile = self.getTileAtPosXY(blank.x+1,blank.y)
        if move == right: tile = self.getTileAtPosXY(blank.x-1,blank.y)
        i,j = blank.index, tile.index
        self.board[i],self.board[j] = self.board[j],self.board[i]
        for index,tile in enumerate(self.board): # set board position of tile
            tile.setBoardPos(index)
    def getStartingBoard(self):
        board = [] # [Tile(1),Tile(2),Tile(3),....Tile(boardlength-1),Tile(None)]
        for name in range(1,self.length)+[None]:
            board.append( Tile(name) )
        for index,tile in enumerate(board): 
            tile.setBoardPos(index)
        return board
    def generateNewPuzzle(self,surface,numSlides):
        print 'generating New Puzzle',self.isSolved()
        self.sequence = []
        lastmove = None
        for i in range(numSlides):
            move = self.getRandomMove(lastmove)
            self.makeMove(move)
            self.sequence.append(move)
            lastmove = move
        #surface.fill(bgcolor) 
        self.drawBoard(surface)
        pygame.display.update()
        pygame.time.wait(50)
    def drawBoard(self,surface):
        map(lambda tile:tile.drawTile(surface), self.board)
#       for tile in self.board:
#           tile.drawTile(surface)
        self.drawBorder(surface)
    def drawBorder(self,surface):
        x,y = converToPixelPos(boardPos(0,0))
        borderwidth,borderheight = boardwidth*tilesize,boardheight*tilesize
        pygame.draw.rect(surface,bordercolor,(x-5,y-5,borderwidth+11,borderheight+11),4)
    def solvePuzzle(self,surface):
        reversemoves = self.sequence[:]
        reversemoves.reverse()
        for move in reversemoves:
            if move == up: rmove = down
            if move == down: rmove = up
            if move == left: rmove = right
            if move == right: rmove = left
            self.makeMove(rmove)
            #surface.fill(bgcolor)
            self.drawBoard(surface)
            pygame.display.update()
            pygame.time.wait(50)
        print 'solve Puzzle ... ', self.isSolved()
    def resetAnimation(self,surface):
        pass


if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode(resolution)
    fpsclock = pygame.time.Clock()
    mb = Board(surface)
    print mb.board
    #surface.fill(bgcolor)
    #mb.drawBoard(surface)
    #pygame.display.update()
    #pygame.time.wait(1000)
    moves = up,down,left,right
    mb.solvePuzzle(surface)
    for i in range(10):
        move = random.choice(moves)
        if mb.isValidMove(move):
            mb.makeMove(move)
            surface.fill(bgcolor)
            mb.drawBoard(surface)
        else:
            print 'Not Valid move'
        if mb.isSolved(): break
        pygame.display.update()
        pygame.time.wait(10)
