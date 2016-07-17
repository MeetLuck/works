import timeit
t = timeit.Timer("soundex1a.soundex('Pilgrim')", 'import soundex1a')
print t.timeit()
print t.repeat(3,2000000)
