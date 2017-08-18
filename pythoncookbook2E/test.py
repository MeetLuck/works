class Descriptor(object):
    def __get__(self,obj,objtype):
#       print 'obj: ', vars(obj)
        print 'obj,objtype', obj,objtype
        try:
            return obj.__dict__['attr']
        except AttributeError:
            return 100
    def __set__(self,obj,value):
        print 'call __set__'
        obj.__dict__['attr'] = value
class Owner(object):
    attr = Descriptor()

if __name__ == '__main__':
    o = Owner()
    print vars(o)
#   o.attr = 10
#   o.attr
    print Owner.attr
    print vars(Owner)
    print Owner.__dict__
    Owner.attr = 100
    print Owner.attr
    print Owner.__dict__
