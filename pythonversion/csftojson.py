# -*- coding: UTF-8 -*-
import sys
import struct
import json

print("Red Alert 2 CSF language converter")
print("by kokutoukiritsugu")
print()

if len(sys.argv) != 3:
    print("error: argument not right!")
    exit()

print("usage: python csftojosn.py csfFilename jsonFilename")
print()

print("input: %s" % sys.argv[1])
print("output: %s" % sys.argv[2])

CSF1 = sys.argv[1]
jCSF = sys.argv[2]

encoding_outfile = 'utf-8'
encoding_CSF_str = 'utf-16le'

sHead_CSF_Converter = 'head_csf_converter'

dCSF = {}

with open(CSF1, mode='rb') as fCSF:
    bHeadCSF, i1, iStringCount1, iStringCount2, i2, i3 = struct.unpack("<4sLLLLL", fCSF.read(24))
    sHeadCSF = bHeadCSF.decode("ascii")

    dCSF[sHead_CSF_Converter] = {}
    dCSF[sHead_CSF_Converter]["HeadCSF"] = sHeadCSF
    dCSF[sHead_CSF_Converter]["UnknowVaule1"] = i1
    # dCSF[sHead_CSF_Converter]["StringCount1"] = iStringCount1
    # dCSF[sHead_CSF_Converter]["StringCount2"] = iStringCount2
    dCSF[sHead_CSF_Converter]["UnknowVaule2"] = i2
    dCSF[sHead_CSF_Converter]["UnknowVaule3"] = i3

    n = 0
    while not n == iStringCount1:
        bHeadStr, i4, iStringLength = struct.unpack("<4sLL", fCSF.read(12))
        bStringKey, = struct.unpack("<%ds" % iStringLength, fCSF.read(iStringLength))
        sStringKey = bStringKey.decode("ascii")
        dCSF[sStringKey] = {}
        dCSF[sStringKey]['HeadStr'] = bHeadStr.decode("ascii")
        dCSF[sStringKey]['UnknowVaule4'] = i4
        # dCSF[sStringKey]['iStringLength'] = iStringLength

        bStringType, = struct.unpack("<4s", fCSF.read(4))
        dCSF[sStringKey]["StringType"] = bStringType.decode("ascii")

        if bStringType:
            iString1ValueLengthRaw, = struct.unpack("<L", fCSF.read(4))
            bString1ValueRaw, = struct.unpack("<%ds" % (iString1ValueLengthRaw * 2), fCSF.read(iString1ValueLengthRaw * 2))
            bString1Value = b''
            for b in bString1ValueRaw:
                bString1Value = bString1Value + (b ^ 0xff).to_bytes(1, "little")
            dCSF[sStringKey]["String1Value"] = bString1Value.decode(encoding_CSF_str)

        if bStringType == b'WRTS':
            iString2ValueLength, = struct.unpack("<L", fCSF.read(4))
            bString2Value, = struct.unpack("<%ds" % iString2ValueLength, fCSF.read(iString2ValueLength))
            dCSF[sStringKey]["String2Value"] = bString2Value.decode("ascii")

        n += 1

j = json.dumps(dCSF, ensure_ascii=False, indent=4)

with open(jCSF, 'w', encoding=encoding_outfile) as f:
    f.truncate()
    f.write(j)
