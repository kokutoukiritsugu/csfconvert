@echo off
path ;
set JAVA_HOME=%cd%\jre8
path=%java_home%\bin\;%path%

java csftotxt ra2md.csf ra2md.csf.txt
java csftotxt stringtable00.csf stringtable00.csf.txt
java csftotxt stringtable01.csf stringtable01.csf.txt