class boardPos:
    def __init__(self,x,y):
        self.x, self.y = x,y
class Tile:
    def __init__(self,name):
        self.name = name
    def setBoardPos(self,boardpos):
        self.boarpos = boardpos
        self.pos = convertToPixelPos(boardpos)
    def drawTile(self,boardpos,number, adjx=0,adjy=0): # draw a tile at board coordinates boardpos
        # optionally a few pixels over (determined by adjx and ajdy)
        left,top = convertToPixelPos(boardpos)
        pygame.draw.rect(surface, tilecolor, (left + adjx, top + adjy, tilesize, tilesize))
        textsurf = basicfont.render( str(number), True, textcolor)
        textrect = textsurf.get_rect()
        textrect.center = left + int(tilesize/2) + adjx, top + int(tilesize/2) + adjy
        surface.blit(textsurf, textrect)
class Board:
    def __init__(self):
        self.length = boardwith*boardheight
        self.board = self.generateNewPuzzle()
    def getBlankTile(self):
        for tile in self.board:
            if tile.name == None:
                return tile
    def startingBoard(self):
        return list(1,self.length) + [None]
    def To2D(self,index):
        return boardPos(index%boardwith, index//boardheight)
    def To1D(self,boardpos):
        return boardpos.x + boardwidth * boardpos.y
    def makeMove(self):
        pass
    def isValidMove(self):
        pass
    def getRandomMove(self):
        pass
    def drawBoard(self):
        pass
    def getTile(self,boardpos):
        index = self.to1D(boardpos)
        return self.board[index]
    def makeMove(self,move):
        blank = self.getBlankTile()
        if move == up:
            tile = board(To1D(
            blank.pos, boardPos(blank.x,blank.y-1)  =  boardPos(blank.x,blank.y+1), blank.pos

    def generateNewPuzzle(self):
        board = [] # [Tile(1),Tile(2),Tile(3),....Tile(boardwidth x boardheight),Tile(None)]
        for index in range(1,self.length)+[None]:
            tile = Tile(index)
            if index == None:
                tile.setPos(self.To2D(self.length))
            else:
                tile.setPos(self.To2D(index))
            board.append(tile)
        return board

