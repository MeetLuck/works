import shlex
#f = open('quotes.txt','rt')
#lines = '''
#This string has embedded "double quotes" and \'single quotes\' in it,\nand even "a \'nested example\'".\n'
#'''
#f.write(lines)
text = """This text says to source quotes.txt before continuing."""
print repr(text)
print

lexer = shlex.shlex(text)
lexer.wordchars += '.'
lexer.source = 'source'

print 'TOKENS:'
for token in lexer:
    print repr(token)
