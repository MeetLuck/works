def add(x,y):
   ''' doctest for function add(x,y)
   >>> add(1,2)
   3
   >>> add(10,20)
   30.0
   >>> assert add(1,2) == 3
   >>> assert add(10,20) == 29 
   '''
   return x + y

if __name__ == '__main__':
    import doctest
    doctest.testmod()
