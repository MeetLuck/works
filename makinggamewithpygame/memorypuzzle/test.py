class Box:
    def __init__(self,*arg):
        print arg, type(arg)
        print arg[0]
        print len(arg)
        if type(arg[0]) == tuple:
            print 'tuple arg:',arg
            self.x,self.y = arg[0]
        else:
            print 'arg:',arg
            self.x, self.y = arg
    def __repr__(self):
        return '(%s,%s)' %(self.x,self.y)


if __name__ == '__main__':
    tu = 2,3
    boxt = Box(tu)
    print boxt
    box = Box(0,1)
    print box
