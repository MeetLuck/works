def reverse_lookup(d,v):
    lst = []
    for k in d:
        if d[k] == v:
            lst.append(k)
    return lst

d = {'a':123,'b':123}
print reverse_lookup(d,123)
#print d,len(d)
