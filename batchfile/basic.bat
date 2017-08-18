@echo off
echo ECHO means REFLECTION
echo pause ^> nul -^> Hit any key to close ...
:: echo redirection and pipe charactoers(^&^<^>^|ON OFF) should be escaped with ^^
set /a num = 1
set /a num = %num% + 1
:: (NoSpace)=(NoSpace)
set name=James Bond
echo %name%
echo %num%
echo .
SETLOCAL ENABLEEXTENSIONS
set me=%~n0
set parent=%~dp0
echo %me%
echo %parent%
:: set name=value
echo filename = %0%
pause > nul
