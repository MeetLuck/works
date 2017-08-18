import pdb
def fn():
    c = 42; pdb.set_trace()
    return c

if __name__ == '__main__':
    fn()
