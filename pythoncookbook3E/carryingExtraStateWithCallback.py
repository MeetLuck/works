# 7.10 Carrying Extra State with Callback Functions

def apply_async(func,callback,*args):
    # compute the result
    result = func(*args)
    # invoke the callback with the result
    callback(result)

def print_result(result):
    print 'Got: ',result

def add(x,y):
    return x+y

def test():
    print apply_async(add,print_result,*(2,3))
    print apply_async(add,print_result,*('hello','world'))

class ResultHandler(object):
    def __init__(self):
        self.sequence = 0
    def handler(self,result):
        self.sequence += 1
        print '[{0}] Got: {1}'.format(self.sequence, result)
    @staticmethod
    def test():
        r = ResultHandler()
        apply_async(add,r.handler,*(2,3))
        apply_async(add,r.handler,*('hello','world'))

def make_handler():
    make_handler.sequence = 0
    def handler(result):
        make_handler.sequence += 1
        print '[{0}] Got: {1}'.format(make_handler.sequence, result)
    return handler

def make_handler_test():
    handler = make_handler()
    apply_async(add, handler, *(2,3))
    apply_async(add, handler, *('hello','world'))


if __name__ == '__main__':
#   test()
#   ResultHandler.test()
    make_handler_test()
