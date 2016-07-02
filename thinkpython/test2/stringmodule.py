import string
punc = list(string.punctuation)
white = list(string.whitespace)
punc_white = list(punc + white)

print '*------------ punctuation ----------------------'
print punc
print '\n*------------ whitespaces ----------------------'
print white
print '\n*------------ punctuation + whitespaces --------'
print punc_white

# ---------- added for test -----------------
