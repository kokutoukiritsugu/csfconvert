@echo off
path ;
set JAVA_HOME=%cd%\jre8
path=%java_home%\bin\;%path%

java txttocsf ra2md.csf.txt ra2md.csf
java txttocsf stringtable00.csf.txt stringtable00.csf
java txttocsf stringtable01.csf.txt stringtable01.csf
