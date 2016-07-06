class Kangaroo(object):
    def __init__(self,contents=None):
        if contents == None:
            contents = []
        self.pouch_contents = contents
    def put_int_pouch(self,obj):
        self.pouch_contents.append(obj)
    def __str__(self):
        ''' returns a string representation of this Kangaroo
        and the contents of the pouch, with one item per line '''
        t = [ object.__str__(self) + ' with pouch contents:' ]
        for obj in self.pouch_contents:
            s = '   ' + object.__str__(obj)
            t.append(s)
        return '\n'.join(t)
    
# test
kang = Kangaroo()
roo = Kangaroo()
kang.put_int_pouch('wallet')
kang.put_int_pouch('car keys')
kang.put_int_pouch(roo)
print kang
print roo
