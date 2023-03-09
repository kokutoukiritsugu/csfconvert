# -*- coding: UTF-8 -*-
import struct
import configobj

csf_name = "ra2.csf"
ini_name = "ra2.csf.ini"
encoding_inifile = 'utf-16le'
encoding_csf_str = 'utf-16le'
open(ini_name, 'w').close()
csffile = open(csf_name, mode='rb')
inifile = configobj.ConfigObj(ini_name, encoding=encoding_inifile)

csfFileHead, unknowIntVaule1, strCount1, strCount2 = struct.unpack("<4sLLL", csffile.read(16))
unknowIntVaule2, unknowIntVaule3 = struct.unpack("<LL", csffile.read(8))
txtstring = 0
while not txtstring == 3:
    strHead, strUnknowVaule, strLong = struct.unpack("<4sLL", csffile.read(12))
    bLBL = struct.unpack("<%ds" % strLong, csffile.read(strLong))
    sLBL = bLBL[0].decode("ascii")
    print(sLBL)
    inifile[sLBL] = {}
    bTYPE = struct.unpack("<4s", csffile.read(4))
    if bTYPE[0] == b' RTS':
        inifile[sLBL]["strMode"] = "STR"
    if bTYPE[0] == b'WRTS':
        inifile[sLBL]["strMode"] = "STRW"
    print(bTYPE)
    bString1Length = struct.unpack("<L", csffile.read(4))
    iString1Length = bString1Length[0] * 2
    bString1raw = struct.unpack("<%ds" % (bString1Length[0] * 2), csffile.read(bString1Length[0] * 2))
    print(bString1raw)
    bString1 = b''
    for b in bString1raw[0]:
        bString1 = bString1 + (b ^ 0xff).to_bytes(1, "little")
    bString1dec = bString1.decode(encoding_csf_str)
    print(bString1dec)
    inifile[sLBL]["string"] = "%s" % bString1.decode(encoding_csf_str)
    if bTYPE[0] == b'WRTS':
        bString2Length = struct.unpack("<L", csffile.read(4))
        bString2 = struct.unpack("<%ds" % bString2Length[0], csffile.read(bString2Length[0]))
        print(bString2)
        inifile[sLBL]["ExtraString"] = "%s" % bString2[0].decode(encoding_csf_str)
    txtstring += 1
inifile.write()
