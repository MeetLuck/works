def mydivmod(x,y):
    if x < 0 : raise Exception('only for x >0')
    Q = 0
    while x >y:
        x = x - y
        Q += 1
    R = x
    return (Q, R)

print mydivmod(5,2)
print mydivmod(2,3)
print mydivmod(-5,2)

