@echo off
path ;
set JAVA_HOME=%cd%\jre8
path=%java_home%\bin\;%path%

:: some java classname
java csftotxt
java txttocsf
