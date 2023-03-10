# -*- coding: UTF-8 -*-
import struct
import configobj

CSF = "ra2.csf"
INI = "ra2.csf.ini"

encoding_INI = 'utf-8'
encoding_CSF_str = 'utf-16le'

open(INI, 'w').close()

fCSF = open(CSF, mode='rb')
fINI = configobj.ConfigObj(INI, encoding=encoding_INI)
fINI.newlines = "\r\n"

bHeadCSF, iUnknowVaule1, iStringCount1, iStringCount2 = struct.unpack("<4sLLL", fCSF.read(16))
iUnknowVaule2, iUnknowVaule3 = struct.unpack("<LL", fCSF.read(8))
sHeadCSF = bHeadCSF.decode("ascii")

fINI[CSF] = {}
fINI[CSF]["HeadCSF"] = sHeadCSF
fINI[CSF]["UnknowVaule1"] = iUnknowVaule1
fINI[CSF]["StringCount1"] = iStringCount1
fINI[CSF]["StringCount2"] = iStringCount2
fINI[CSF]["UnknowVaule2"] = iUnknowVaule2
fINI[CSF]["UnknowVaule3"] = iUnknowVaule3

print(fINI[CSF])

print()

n = 0
while not n == iStringCount1:
    bHeadStr, iUnknowVaule4, iStringLength = struct.unpack("<4sLL", fCSF.read(12))
    sHeadStr = bHeadStr.decode("ascii")

    bStringKey = struct.unpack("<%ds" % iStringLength, fCSF.read(iStringLength))
    sStringKey = bStringKey[0].decode("ascii")
    print(sStringKey)
    print()
    fINI[sStringKey] = {}

    bStringType = struct.unpack("<4s", fCSF.read(4))
    print(bStringType)
    print()
    if bStringType[0] == b' RTS':
        fINI[sStringKey]["StringType"] = "STR"
    if bStringType[0] == b'WRTS':
        fINI[sStringKey]["StringType"] = "STRW"

    if bStringType[0]:
        bString1ValueLength = struct.unpack("<L", fCSF.read(4))
        iString1ValueLength = bString1ValueLength[0] * 2
        print(bString1ValueLength)
        bString1ValueRaw = struct.unpack("<%ds" % (bString1ValueLength[0] * 2), fCSF.read(bString1ValueLength[0] * 2))
        bString1Value = b''
        for b in bString1ValueRaw[0]:
            bString1Value = bString1Value + (b ^ 0xff).to_bytes(1, "little")
        sString1Value = bString1Value.decode(encoding_CSF_str)
        print(sString1Value)
        print()
        fINI[sStringKey]["String1Value"] = "%s" % sString1Value

    if bStringType[0] == b'WRTS':
        bString2ValueLength = struct.unpack("<L", fCSF.read(4))
        print(bString2ValueLength)
        bString2Value = struct.unpack("<%ds" % bString2ValueLength[0], fCSF.read(bString2ValueLength[0]))
        print(bString2Value)
        sString2Value = bString2Value[0].decode("ascii")
        print(sString2Value)
        fINI[sStringKey]["String2Value"] = "%s" % sString2Value

    n += 1


fINI.write()
