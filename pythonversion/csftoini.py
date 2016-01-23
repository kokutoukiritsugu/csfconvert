# -*- coding: UTF-8 -*-
import struct
import configobj

csffile = open("ra2.csf", mode='rb')
inifile = configobj.ConfigObj("ra2.csf.ini", encoding="UTF-8")
csfFileHead, unknowIntVaule1, strCount1, strCount2 = struct.unpack("<4sLLL", csffile.read(16))
unknowIntVaule2, unknowIntVaule3 = struct.unpack("<LL", csffile.read(8))
txtstring = 0
while not txtstring == strCount1:
    strHead, strUnknowVaule, strLong = struct.unpack("<4sLL", csffile.read(12))
    strLBL = struct.unpack("<%ds" % strLong, csffile.read(strLong))
    inifile["%s" % strLBL[0].decode("utf-8")] = {}
    strRtsHead = struct.unpack("<4s", csffile.read(4))
    if strRtsHead[0] == b' RTS':
        inifile["%s" % strLBL[0].decode("utf-8")]["strMode"] = "STR"
    if strRtsHead[0] == b'WRTS':
        inifile["%s" % strLBL[0].decode("utf-8")]["strMode"] = "STRW"
    strRtsLength = struct.unpack("<L", csffile.read(4))
    strRtsLengthInt = strRtsLength[0] * 2
    strRts = struct.unpack("<%ds" % (strRtsLength[0] * 2), csffile.read(strRtsLength[0] * 2))
    strRtsInvert = bytearray(strRts[0])
    while not 0 == strRtsLengthInt:
        strRtsInvert[strRtsLengthInt - 1] = strRtsInvert[strRtsLengthInt - 1] ^ 0xff
        strRtsLengthInt -= 1
    inifile["%s" % strLBL[0].decode("utf-8")]["string"] = "%s" % strRtsInvert.decode("UTF-16LE")
    if strRtsHead[0] == b'WRTS':
        strRtsExtraLength = struct.unpack("<L", csffile.read(4))
        strRtsExtraStr = struct.unpack("<%ds" % strRtsExtraLength[0], csffile.read(strRtsExtraLength[0]))
        inifile["%s" % strLBL[0].decode("utf-8")]["ExtraString"] = "%s" % strRtsExtraStr[0].decode("UTF-8")
    txtstring += 1
inifile.write()
