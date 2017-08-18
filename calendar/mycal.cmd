@echo off
calendar20.py
:while1
title %date% %time:~0,5%
::ping -n seconds 127.0.0.1 >nul
ping -n 60 127.0.0.1 >nul
goto :while1
