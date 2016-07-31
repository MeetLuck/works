# define function
def myzip(seq1,seq2):
    length = min( len(seq1), len(seq2) )
#   result = list()
#   for i in range(length):
#       t = seq1[i], seq2[i]
#       result.append(t)
#   result = [ (seq1[i],seq2[i]) for i in range(length) ]
    return result

if __name__ == '__main__':
    print myzip([1,2,3],['a','b'])
