import sys
from termcolor import colored, cprint
text = colored('---- test text','red',attrs=['reverse','blink'])
print text
cprint('---test text','green','on_red')
