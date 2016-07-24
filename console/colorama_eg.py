
'ANSI.SYS for command.com(MSDOS)'
"So it's not possible to use ANSI.SYS for cmd.exe"

import colorama
colorama.init()
 

import sys
sys.stdout.write("\033[33mYellow Submarine")
sys.stdout.write("\n")
sys.stderr.write("\033[31mred, red , wine!")
sys.stdout.write("\n")

print '\033[0;31mGray like Ghost\033[1;m'
print '\033[1;31mRed like Radish\033[1;m'
print '\033[4;31mGreen like Grass\033[1;m'
print '\033[5;31mYellow like Yolk\033[1;m'
print '\033[8;31mBlue like Blood\033[1;m'
print '\033[1;35mMagenta like Mimosa\033[1;m'
print '\033[1;36mCyan like Caribbean\033[1;m'
print '\033[1;37mWhite like Whipped Cream\033[1;m'
print '\033[1;38mCrimson like Chianti\033[1;m'
print '\033[1;41mHighlighted Red like Radish\033[1;m'
print '\033[1;42mHighlighted Green like Grass\033[1;m'
print '\033[1;43mHighlighted Brown like Bear\033[1;m'
print '\033[1;44mHighlighted Blue like Blood\033[1;m'
print '\033[1;45mHighlighted Magenta like Mimosa\033[1;m'
print '\033[1;46mHighlighted Cyan like Caribbean\033[1;m'
print '\033[1;47mHighlighted Gray like Ghost\033[1;m'
print '\033[1;48mHighlighted Crimson like Chianti\033[1;m'

class style:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
class fg:
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'
class bg:
    black='\033[40m'
    red='\033[41m'
    green='\033[42m'
    orange='\033[43m'
    blue='\033[44m'
    purple='\033[45m'
    cyan='\033[46m'
    lightgrey='\033[47m'

#print style.reset
print 'reset ...'
def red(name):
    sys.stdout.write(style.reset)
    sys.stdout.write(fg.lightred)
    sys.stdout.write(bg.lightgrey)
#   text = "{0.red}{1}{2.reset}".format(fg,name,style)
    print name
#   print ("\033[91m{}\033[00m" .format(name))
red('red text expected1')
#sys.stdout.write('\033[2J')
red('red text expected1')
print "\33[0;31;4mDimRedBack"
print "\33[0;31;4mDimRedBack"

