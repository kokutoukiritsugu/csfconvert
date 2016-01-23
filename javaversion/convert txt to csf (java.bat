@echo off
path ;
set JAVA_HOME=%cd%\jre8
path=%java_home%\bin\;%path%

java txttocsf ra2md.csf.txt ra2md.csf

java txttocsf stringtable00.csf.txt stringtable00.csf
java txttocsf stringtable01.csf.txt stringtable01.csf

java txttocsf stringtable96.csf.txt stringtable96.csf
java txttocsf stringtable97.csf.txt stringtable97.csf
java txttocsf stringtable98.csf.txt stringtable98.csf
java txttocsf stringtable99.csf.txt stringtable99.csf