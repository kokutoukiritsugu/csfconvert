# -*- coding: UTF-8 -*-
import struct
import configobj

inifile = configobj.ConfigObj("ra2.ini", encoding="UTF-8")
print(inifile['Brief:SOV09']['string'])
inifile.keys
print(inifile.keys)
