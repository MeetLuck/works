class Wave:
    pass
class Motive(Wave):
    def set_subwaves(self,*args,**kwargs):
        if impulse: # 5-3-5-3-5 
            self.i   = Motive()
            self.ii  = Corrective()
            self.iii = Motive()
            self.iv  = Corrective()
            self.v   = Motive()
        else diagonal: # 3-3-3-3-3(wedge)
            self.i   = Corrective()
            self.ii  = Corrective()
            self.iii = Corrective()
            self.iv  = Corrective()
            self.v   = Corrective()
class Impulse(Motive):
    def set_subwaves(self,**points):
            self.i   = Motive(p0,p1)
            self.ii  = Corrective(p1,p2)
            self.iii = Motive(p2,p3)
            self.iv  = Corrective(p3,p4)
            self.v   = Motive(p4,p5)
class Diagonal(Motive):
    def set_subwaves(self,**points):
            self.i   = Corrective(p0,p1)
            self.ii  = Corrective(p1,p2)
            self.iii = Corrective(p2,p3)
            self.iv  = Corrective(p3,p4)
            self.v   = Corrective(p4,p5)


class Corrective:
    def set_subwaves(self,*args, **kwargs):
        if zigzag: # 5-3-5
            self.a = Motive()
            self.b = Corrective()
            self.c = Motive()
        elif flat: # 3-3-5
            self.a = Corrective()
            self.b = Corrective()
            self.c = Motive()
        elif double_zigzag: # 3-3-3
            self.a = Corrective()
            self.b = Corrective()
            self.c = Corrective()
        elif triangle: # 3-3-3-3-3
            self.a = Corrective()
            self.b = Corrective()
            self.c = Corrective()
            self.d = Corrective()
            self.e = Corrective()

class ZigZag(Corrective):
    def set_subwaves(self,**points):
        self.a = Motive(p0,pa)
        self.b = Corrective(pa,pb)
        self.c = Motive(pb,pc)
class Flat(Corrective):
    def set_subwaves(self,**points):
        self.a = Corrective(p0,pa)
        self.b = Corrective(pa,pb)
        self.c = Motive(pb,pc)
class Double_ZigZag(Corrective):
    def set_subwaves(self,**points):
        self.a = Corrective(p0,pa)
        self.b = Corrective(pa,pb)
        self.c = Corrective(pb,pc)
class Triangle(Corrective):
    def set_subwaves(self,**points):
        self.a = Corrective(p0,pa)
        self.b = Corrective(pa,pb)
        self.c = Corrective(pb,pc)
        self.d = Corrective(pb,pc)
        self.e = Corrective(pb,pc)

