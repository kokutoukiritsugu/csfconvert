# -*- coding: UTF-8 -*-
import struct
import configobj

csf_name = "ra2.csf"
ini_name = "ra2.csf.ini"
encoding_inifile = 'utf-8'
encoding_csf_str = 'utf-16le'
open(ini_name, 'w').close()
csffile = open(csf_name, mode='rb')
inifile = configobj.ConfigObj(ini_name, encoding=encoding_inifile)
inifile.newlines = "\r\n"

bHEADcsf, unknowIntVaule1, strCount1, strCount2 = struct.unpack("<4sLLL", csffile.read(16))
unknowIntVaule2, unknowIntVaule3 = struct.unpack("<LL", csffile.read(8))
sHEADcsf = bHEADcsf.decode("ascii")

inifile[csf_name] = {}
inifile[csf_name]["head"] = sHEADcsf
inifile[csf_name]["unknowIntVaule1"] = unknowIntVaule1
inifile[csf_name]["strCount1"] = strCount1
inifile[csf_name]["strCount2"] = strCount2
inifile[csf_name]["unknowIntVaule2"] = unknowIntVaule2
inifile[csf_name]["unknowIntVaule3"] = unknowIntVaule3

print(inifile[csf_name])

print()

txtstring = 0
while not txtstring == strCount1:
    strHead, strUnknowVaule, strLong = struct.unpack("<4sLL", csffile.read(12))
    bLBL = struct.unpack("<%ds" % strLong, csffile.read(strLong))
    sLBL = bLBL[0].decode("ascii")
    print(sLBL)
    print()
    inifile[sLBL] = {}

    bTYPE = struct.unpack("<4s", csffile.read(4))
    print(bTYPE)
    print()
    if bTYPE[0] == b' RTS':
        inifile[sLBL]["strMode"] = "STR"
    if bTYPE[0] == b'WRTS':
        inifile[sLBL]["strMode"] = "STRW"

    bString1Length = struct.unpack("<L", csffile.read(4))
    iString1Length = bString1Length[0] * 2
    bString1raw = struct.unpack("<%ds" % (bString1Length[0] * 2), csffile.read(bString1Length[0] * 2))
    bString1 = b''
    for b in bString1raw[0]:
        bString1 = bString1 + (b ^ 0xff).to_bytes(1, "little")
    sString1 = bString1.decode(encoding_csf_str)
    print(sString1)
    print()
    inifile[sLBL]["string"] = "%s" % sString1

    if bTYPE[0] == b'WRTS':
        bString2Length = struct.unpack("<L", csffile.read(4))
        bString2 = struct.unpack("<%ds" % bString2Length[0], csffile.read(bString2Length[0]))
        sString2 = bString2[0].decode("ascii")
        print(sString2)
        inifile[sLBL]["ExtraString"] = "%s" % sString2

    txtstring += 1


inifile.write()
