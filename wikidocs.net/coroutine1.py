''' 5.3 Coroutines 
    from http://wla.berkeley.edu/~cs61a/fa11/lectures/streams.html#coroutines
'''
import os
cls = lambda : os.system('cls')

################## python coroutine ##############################
def match(pattern):
    print "... Looking for '{pattern}'".format(pattern=pattern)
    try:
        while True:
            s = yield
            print 'receiving {data}'.format(data = s)
            print 'processing {data}'.format(data = s)
            if pattern in s:
                print '-> found in {s}'.format(s=s)
            else:
                print '... not found ...'
    except GeneratorExit:
        print '===== Done ====='

m = match('work')
m.next()
m.send("I'm working on it")
m.send("What are you searching")
m.send("my generator looking for word 'work'")
m.send("Did you find it")
m.close()
cls()

##################### produce, filter, and consume ###########################
'''
                                                      
   +---------+  send  +--------+   send      +--------+  send  +----------+
   | producer|    ->  | filter |  -> ...  -> | filter |   ->   | consumer |
   +---------+        +--------+             +--------+        +----------+
 
'''
##############################################################################

def read(text, next_coroutine):
    print text
    for word in text.split():
        print 'sending -> {word}'.format(word=word)
        next_coroutine.send(word)
    next_coroutine.close()

text = 'Commending spending is offending to people pending lending!'
matcher = match('ing')
matcher.next()
read(text, matcher)

cls()
def match_filter(pattern,next_coroutine):
    print 'Looking for {pattern}'.format(pattern=pattern)
    try:
        while True:
            s = yield   # receive data
            if pattern in s:
                next_coroutine.send(s) # send matching word to next_coroutine
    except GeneratorExit:
        next_coroutine.close()
def print_consumer():
    print 'Preparing to print'
    try:
        while True:
            line = yield
            print line
    except GeneratorExit:
        print '===== Done ======'

printer = print_consumer()
printer.next()
matcher = match_filter('ing',printer)
matcher.next()
read(text, matcher)
cls()
def count_letters(next_coroutine):
    try:
        while True:
            s = yield
            print 'received <- {s}'.format(s=s)
            counts = {letter:s.count(letter) for letter in set(s)}
            next_coroutine.send(counts)
    except GeneratorExit as e:
        next_coroutine.close()

def sum_dictionaries():
    total = dict()
    try:
        while True:
            counts = yield
            print counts
            for letter, count in counts.items():
                total[letter] = total.get(letter,0) + count
    except GeneratorExit:
        max_letter = max(total.items(), key=lambda t: t[1])
        print max_letter
        print "Most frequent letter is '{max_letter}'".format(max_letter=max_letter[0])

s = sum_dictionaries()
s.next()
c = count_letters(s)
c.next()
read(text,c)
cls()
print 'Multitasking'
def read_to_many(text, coroutines):
    for word in text.split():
        for coroutine in coroutines:
            print "send '{word}' to {coroutine}".format(word=word, coroutine=coroutine.__name__)
            coroutine.send(word)
    for coroutine in coroutines:
        coroutine.close()
m = match('ing'); m.next()
p = match('pe'); p.next()
read_to_many(text, [m,p])
