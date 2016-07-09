import os, sys
home = os.getenv('HOME')
song = os.path.join(home,'song')
fileList = [ f for f in os.listdir(song) ]
print song
print fileList
fileList2 = [ os.path.join(song,f) for f in fileList ]
print '*'*80
print fileList2
print '*'*80
fileList3 = [ f for f in fileList2 if os.path.splitext(f)[1] =='.mp3' ]
fileList4 = [ f for f in fileList2 if os.path.splitext(f)[1] =='.flac' ]
print '*'*80
print fileList3
print '*'*80
print fileList4
