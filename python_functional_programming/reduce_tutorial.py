lst1 = range(1,6)

def test(*args, **kwargs):
    print args, kwargs
test(1,2,3,x=10,u=20)
def sum_power( total,value,power=1 ):
    print 'sum:%s, input: %s, power: %s ' %(total,value,power)
    return total + pow(value,power)

from functools import partial
sum2 = partial(sum_power,power=2)
sum3 = partial(sum_power,power=3)

print reduce(sum2, lst1,0)
print reduce(sum3, lst1,0)

