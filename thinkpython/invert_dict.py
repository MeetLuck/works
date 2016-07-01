from counters import histogram
def inver_dict(d):
    inv = {}
    for key in d:
        val = d[key]
        if val not in inv:
            inv[val] = [key]
        else:
            inv[val].append(key)
    return inv

hist = histogram('parrot')
print hist
inv = inver_dict(hist)
print inv
