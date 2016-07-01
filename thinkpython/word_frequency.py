import string

''' chapter 13 case study: data structure selection '''
#--------- word frequency analysis -----------------

def process_file(filename):
    hist = dict()
    fp = open(filename)
    for line in fp:
        process_line(line,hist)
    return hist

def process_line(line, hist):
    line = line.replace('-',' ')
    for word in line.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        hist[word] = hist.get(word,0) + 1

def total_words(hist):
    return sum( hist.values() )
def different_words(hist):
    return len(hist)



hist = process_file('emma')
print 'Total number of words: ', total_words(hist)
print 'Number of different words: ', different_words(hist)

#---------- 13.4 Most common words ------------------
def most_common(hist):
    t = []
    for key, value in hist.items():
        t.append( (value,key) )
    t.sort(reverse=True)
    return t

t = most_common(hist)
print 'The most common words are:'
for freq, word in t[0:10]:
    print word, '\t', freq

#---------------- Optional parameters --------------
def print_most_common(hist, num=10):
    t = most_common(hist)
    print 'The most common words are:'
    for freq, word in t[:num]:
        print word, '\t', freq
print_most_common(hist,20)
#print hist
#----------- dictionary substraction --------------
def substract(d1,d2):
    res = dict()
    for key in d1:
        if key not in d2:
            res[key] = None
    return res

words = process_file('words.txt')
diff = substract(hist, words)
print 'The words in the book that are not in the word list are: '
for word in diff.keys():
    print word,

''' 13.7 Random words '''
import random
def random_word(h):
    t = list()
    for word, freq in h.items():
        t.extend( [word]*freq )
    return random.choice(t)

for i in range(10):
    print '#---- random word from emma.txt\n'
    print random_word(hist)
