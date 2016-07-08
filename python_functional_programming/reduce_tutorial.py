lst1 = range(1,6)

def sum_power1( total,value,power=1 ):
    print 'sum:%s, input: %s, power: %s ' %(total,value,power)
    return total + pow(value,power)

def sum_power2(power):
    return lambda sum,value,power=power: sum + pow(value,power)

def sum_power3(power):
    print 'calling %s' %sum_power3
    def wrapper(sum,value):
        print 'sum:%s, input: %s, power: %s ' %(sum,value,power)
        return sum + pow(value,power)
    return wrapper

from functools import partial
sum2 = partial(sum_power1,power=2)
sum3 = partial(sum_power1,power=3)

print reduce(sum2, lst1,0)
print reduce(sum3, lst1,0)

print reduce(sum_power2(2), lst1, 0)
print reduce(sum_power2(3), lst1, 0)

print reduce( sum_power3(2), lst1, 0)
print reduce( sum_power3(3), lst1, 0)

#---------- using map --------------
lst_squared = map(lambda x:x*x, lst1)
lst_cubed = [ pow(x,3) for x in lst1 ]
print lst_squared,sum(lst_squared)
print lst_cubed, sum(lst_cubed)
