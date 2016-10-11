class Map(object):
    def __init__(self,amap):
        self.amap = amap
    def __getitem__(self,xy):
        x,y = xy
        print x,y
        return self.amap[y][x]

if __name__ == '__main__':
    li = [
            [1,2,3],
            [4,5,6],
            [7,8,9]
            ]
    amap = Map(li)
    print amap[(1,2)] == amap[1,2]
    print amap[0,0],amap[0,1]
