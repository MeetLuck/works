class C(object):
  def __getattribute__(self,name):
      print 'calling __getattribute__'
      return object.__getattribute__(self,name)
  def __getattr__(self,name):
      print 'calling __getattr__'
      if name == 'notfound': return -99
      else: raise AttributeError, name + ' not allowed'

if __name__ == '__main__':
    c = C()
    print c.notfound
