# color [bg][fg]
# color [fg]
# 0 8   black   gray
# 1 9   blue    light blue
# 2 A   green   light green
# 3 B   aqua    light aqua
# 4 C   red     light red
# 5 D   purple  light purple
# 6 E   yellow  light yellow
# 7 F   white   light white
# if no argument given, color restores the color to what it was when CMD.EXE started.

import os
os.system('color 80')
print 'white bg - black fg'
os.system('color')
print 'restore system color'
