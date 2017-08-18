@echo off
set /a x=1,y=2,z=x+y
echo %x%,%y%,%z%
set /a k=!x
echo %k%

CALL :func_square 3
ECHO result=%result%

:func_square
SETLOCAL
SET a=%1
SET /A y=a*a
ENDLOCAL & SET result=%y%
