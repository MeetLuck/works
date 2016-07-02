def histogram(string):
    d = {}
    for char in string:
        if char not in d:
            d[char] = 1
        else:
            d[char] += 1
    return d

def dic_get_value(dic, key,default):
    ''' d.get(key [,default] ) '''
    if key not in dic:
        return default
    elif key in dic:
        return dic[key]
    else:
        raise Exception('unknown error')

def histogram_v2(string):
    d = {}
    for char in string:
        d[char] = dic_get_value(d, char,0) + 1
    return d

def print_hist(dic):
    for key in dic:
        print key, dic[key]

h= histogram('aabbac')
print_hist(h)
h2 =  histogram_v2('aabbac')
print_hist(h2)
