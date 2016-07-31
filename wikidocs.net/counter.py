def counter(string):
    counter = dict()
    for c in in_str:
    #   if counter.has_key(c):
    #       counter[c] += 1
    #   else:
    #       counter[c] = 1
        counter[c] = counter.get(c,0) + 1
    return counter
def histogram(dic):
    for key,value in dic.items():
        print "{} :  {}".format(key,'*' * value)

if __name__ == '__main__':
    in_str = list("aiifwiefawifaifwahfiawfthis is a counter")
#   print counter(in_str)
    histogram( counter(in_str) )

