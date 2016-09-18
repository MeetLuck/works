# terminate() to quit game
# checkForQuit() to check 'quit' condition
# getStartingBoard() to return board[[1,4,7],[2,5,8],[3,6,None]] 
# getBlankPosition(board) to return boardpos
# makeMove(board,move) to move board according to 'up','down','left','right' 
# isValidMove(board,move) to check validate move
# getRandomMove(board,lastMove=None) to return a random move from the list of moves 
# converToPixelPos(boardX,boardY) to convert board coordinates to pixel cooridinates
# drawTile(boardX,boardY,number,adjx=0,adjy=0) to draw tile
# makeText(text,color,bgcolor,top,left) to return text surface,textrect
# drawBoard(board,message) to draw board
# generateNewPuzzle(numSlides) to return random-like board and sequence
resolution = 640,480
width,height = resolution
boardwidth,boardheight = 3,3
tilesize = 80
fps = 30
blank = None

# R G B colors
black = 0,0,0
white = 255,255,255
blightblue = 0,50,255
darkturquoise = 3,54,73
green = 0,204,0
red = 255,0,0

bgcolor = darkturquoise
tilecolor = green
textcolor = white
bordercolor = blightblue
blankcolor = list(bgcolor); blankcolor[1] += +10; blankcolor = tuple(blankcolor)
basicfontsize = 20

buttoncolor = white
buttontextcolor = black
messagecolor = white

xmargin = int( (width - (tilesize*boardwidth + boardwidth-1))/2 )
ymargin = int( (height - (tilesize * boardheight + boardheight - 1))/2 )

up,down,left,right = 'up','down','left','right' 

