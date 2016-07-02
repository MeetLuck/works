import pickle
''' Pickling translates almost any type of object into a string
    suitable for storage in a database, and then translates strings back into objects
    '''
t1 = [1,2,3]
s = pickle.dumps(t)
t2 = pickle.loads(s)
print repr(s)
print t2
