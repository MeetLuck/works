@ECHO OFF
IF "%var1%"=="" SET var1=10
IF NOT DEFINED var2 SET var2=20

SET var3=Hello
IF "%var3%"=="Hello" ECHO %var3%
IF /I "%var3%"=="hello" ECHO %var3%
SET /A var4=100
IF '%var4%' EQU "100" ECHO var4 == %var4% 
IF '%var4%' NEQ "99"  ECHO var4 != 100
IF '%var4%' GEQ "100" ECHO var4 ^>= 100
IF '%var4%' LEQ "100" ECHO var4 ^<= 100

echo %%
echo ^^
echo ^>
echo ^<
echo ^|
cls
echo script Name      : %~n0 
echo Full script name : %~f0 
echo file eXtension   : %~x0 
echo Parent directory : %~dp0 
echo first arguemnt   : %1 
set name="Johnson & son"
echo name=%name%
echo.
:: continuation character "^" 
set /A x=1
IF "%x%" EQU "1" ^
ECHO x equals %x% &^
ECHO Indeed, equal
SET /A modulo=14%%3
ECHO 14//3 = %modulo%
