class Pos:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __str__(self):
        return 'Pos(%s,%s)' %(self.x,self.y)
class Box:
    def __init__(self,pos):
        self.x,self.y = pos.x, pos.y
        self.pos = Pos(self.x,self.y)

if __name__ == '__main__':
    box = Box(Pos(0,0))
    print box.x,box.y
    print box.pos
    box.x += 1
    print box.x,box.y
    print box.pos
