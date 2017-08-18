# redirection
C:\>command > filename      'Redirect command output to a file'    
C:\>command >> filename     'APPEND into a file'    
C:\>command < filename      'Type a text file and pass the text to command'   
C:\>commandA | commandB     'Pipe the output from commandA into commandB'    
C:\>commandA & commandB     'Run commandA and then run commandB'    
C:\>commandA && commandB    'Run commandA, if it succeeds then run commandB'    
C:\>commandA || commandB    'Run commandA, if it fails then run commandB'    
C:\>commandA && commandB || commandC  'If commandA succeeds run commandB, if it fails commandC'   

C:\>command 2> file           'Redirect any error message into a file'
C:\>command 2>> file          'Append any error message into a file'
C:\>(command) 2> file         'Redirect any CMD.exe error into a file'
C:\>command > file 2>&1       'Redirect errors and output to one file'
C:\>command > fileA 2> fileB  'Redirect output and errors to separate files'

C:\>command 2> nul              'Redirect error messages to NUL'
C:\>command > nul 2>&1          'Redirect error and output to NUL'
C:\>command > filename 2> nul   'Redirect output to file but suppress error'
C:\>command) > filename 2> nul  'Redirect output to file but suppress CMD.exe errors'

Redirect multiple lines by bracketing a set of commands:
(
  Echo sample text1
  Echo sample text2
) > C:\logfile.txt 

group expression by parenthesis
(command)
(
    command
    command
)

IF EXIST C:\pagefile.sys (
    ECHO pagefile found on C drive
)

SET var=abcabc
# replace the character string 'ab' with 'xy'
ECHO %var:ab=xy%
# delete the character string 'ab'
ECHO %var:ab=%

SET var=123456789abcdef

'Extract only the first 5 characters'
echo %var:~0,5%     # 12345
'Skip 7 characters and then extract the next 5'
echo %var:~7,5%     # 89abc
'Skip 7 characters and then extract everything else'
echo %var:~7%       # 89abcdef0
'Extract only the last 7 characters'
echo %var:~-7%      # abcdef0
'Extract everything BUT the last 7 characters'
echo %var:~0,-7%    # 123456789

Test if a variable is empty

'test for the existence of a command line parameter - use empty brackets'
IF (%1)==() command
IF not (%1) EQU () command

'test for NULL'
IF NOT DEFINED command

'test the existence of files and folders'
IF EXIST filename   command

'IF¡¦ ELSE¡¦ commands'

IF EXIST filename.txt (
    Echo deleting filename.txt
    Del filename.txt
 ) ELSE ( 
    Echo The file was not found.
 )


Parameter Extensions
f for Full path,d for Drive, p for Path, n for fileName without extension, x for eXtension only
a for file Attributes,  z for file siZe

%~f1 'Expand %1 to a Fully qualified path name - C:\utils\MyFile.txtr'
%~d1 'Expand %1 to a Drive letter only - C:'
%~p1 'Expand %1 to a Path only e.g. \utils\ ' 
%~n1 'Expand %1 to a file Name without file extension C:\utils\MyFile'
%~x1 'Expand %1 to a file eXtension only - .txt'
%~s1 'Short 8.3 name (if it exists.)'
%~1  'Expand %1 removing any surrounding quotes (")'
%~a1 'Display the file attributes of %1'
%~t1 'Display the date/time of %1'
%~z1 'Display the file size of %1'
%~dp1 'Expand %1 to a drive letter and path only'
%~sp1 'Expand %1 to a path shortened to 8.3 characters'
%~nx2 'Expand %2 to a file name and extension only'


'In a batch, the command must use a double percent sign.'
FOR %%i IN (1,2,3) DO ECHO %%i
'From a command line, echoes 1, 2, and 3.'
FOR %i IN (1,2,3) DO @ECHO %i
'Echoes file names of files in the current folder and having the .txt extension.'
FOR %i IN (*.txt) DO @ECHO %i
'Echoes file names matching the pattern.'
FOR %i IN ("C:\Windows\system32\*.exe") DO @ECHO %i
'Recursive loop' 
FOR /R %i IN (*.txt) DO @ECHO %i
'Echoes the names of all Directory'
FOR /D %i IN (*) DO @ECHO %i
'Echoes the numbers from 1 to 10.'
FOR /L %i IN (1,1,10) DO @ECHO %i


for /f "tokens=1-3 delims=:" %a in ("First:Second::Third") do @echo %a-%b-%c
Parses a string into tokens delimited by ":".
The quotation marks indicate the string is not a file name.
The second and third tokens are stored in %b and %c even though %b and %c are not expressly mentioned in the part of the command before "do".
The two consecutive colons are treated as one separator; %c is not "" but rather "Third".
Does some of the job of the cut command from other operating systems.

'For each line in a file, echoes the line.'
FOR /F "tokens=*" %i IN (list.txt) DO @ECHO %i
'For each line in the files, echoes the line.'
FOR /F "tokens=*" %i IN (list1.txt list2.txt) DO @ECHO %i
