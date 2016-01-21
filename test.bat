@echo off
java csftotxt ra2md.csf ra2md.csf.txt
java csftotxt stringtable00.csf stringtable00.csf.txt
java csftotxt stringtable01.csf stringtable01.csf.txt

java txttocsf ra2md.csf.txt ra2md.1.csf
java txttocsf stringtable00.csf.txt stringtable00.1.csf
java txttocsf stringtable01.csf.txt stringtable01.1.csf