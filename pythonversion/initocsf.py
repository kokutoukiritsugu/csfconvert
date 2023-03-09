# -*- coding: UTF-8 -*-
import struct
import configobj

csf_name = "ra2.csf"
csf2_name = "ra2_2.csf"
ini_name = "ra2.csf.ini"
encoding_inifile = 'utf-8'
encoding_csf_str = 'utf-16le'
open(csf2_name, 'w').close()

inifile = configobj.ConfigObj(ini_name, encoding=encoding_inifile)
inifile.newlines = "\r\n"

print(inifile.keys)
s = inifile[csf_name]
print(s)