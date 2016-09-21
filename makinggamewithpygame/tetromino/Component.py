from constants import *
class BoardPos:
    def __init__(self,x,y):
        self.x,self.y = x,y
class NewPiece:
    def __init__(self):
        self.shape = random.choice(pieces)
        self.pos = 0,0
        self.color = random.choice(colors)
class Board:
    def __init__(self):
        self.width = boardwidth
        self.height = boardheight
        self.length = self.width * self.height
        self.board = self.generateNewBoard()

    def draw(self): #,surface):
        for index,box in enumerate(self.board):
            boardpos = self.converTo2D(index)
            print self.board[index],
            if boardpos.x % self.width == 0:
                print
    def makeMove(self,move):
        pass

    def generateNewBoard(self):
        return [blank] * self.length

    def converTo2D(self,index):
        return BoardPos(index % self.width, index // self.width)

if __name__ == '__main__':
    mb = Board()
    mb.draw()
