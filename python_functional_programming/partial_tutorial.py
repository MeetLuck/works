def partial1(func, *partial_args):
    def wrapper(*extra_args):
        print 'partial_args: %s,  extra_args: %s' %(partial_args,extra_args)
        args = list(partial_args)
        args.extend(extra_args)
        print args
        return func(*args)
    return wrapper

def test_partial(*args):
    print args, sum(args)
partial1(test_partial, 10)(20)
