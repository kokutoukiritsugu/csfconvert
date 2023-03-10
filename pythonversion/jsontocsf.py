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

print("usage: python jsontocsf.py jsonFilename csfFilename")
print()

print("input: %s" % sys.argv[1])
print("output: %s" % sys.argv[2])

CSF2 = sys.argv[2]
jCSF = sys.argv[1]

encoding_outfile = 'utf-8'
encoding_CSF_str = 'utf-16le'

sHead_CSF_Converter = 'head_csf_converter'

dCSF = {}

with open(jCSF, 'r', encoding=encoding_outfile) as json_file:
    dCSF = json.load(json_file)

with open(CSF2, 'wb') as fCSF:
    sHeadCSF = dCSF[sHead_CSF_Converter]['HeadCSF']
    i1 = dCSF[sHead_CSF_Converter]['UnknowVaule1']
    i2 = dCSF[sHead_CSF_Converter]['UnknowVaule2']
    i3 = dCSF[sHead_CSF_Converter]['UnknowVaule3']
    iStringCount1 = len(dCSF) - 1
    iStringCount2 = iStringCount1
    p = struct.pack("<4sLLLLL", bytes(sHeadCSF, encoding='ascii'), i1, iStringCount1, iStringCount2, i2, i3)
    fCSF.write(p)

    for sStringKey in dCSF:
        if sStringKey == sHead_CSF_Converter:
            continue

        sHeadStr = dCSF[sStringKey]['HeadStr']
        i4 = dCSF[sStringKey]['UnknowVaule4']
        iStringLength = len(sStringKey)
        p = struct.pack("<4sLL%ds" % iStringLength, bytes(sHeadStr, encoding='ascii'), i4, iStringLength, bytes(sStringKey, encoding='ascii'))
        fCSF.write(p)

        sStringType = dCSF[sStringKey]['StringType']
        sString1Value = dCSF[sStringKey]['String1Value']

        if sStringType:
            bString1Value = bytes(sString1Value, encoding=encoding_CSF_str)
            bString1ValueRaw = b''
            for b in bString1Value:
                bString1ValueRaw = bString1ValueRaw + (b ^ 0xff).to_bytes(1, "little")
            iString1ValueLength = len(bString1ValueRaw)
            iString1ValueLengthRaw = iString1ValueLength // 2
            sStringType = dCSF[sStringKey]["StringType"]
            p = struct.pack("<4sL%ds" % iString1ValueLength, bytes(sStringType, encoding='ascii'), iString1ValueLengthRaw, bString1ValueRaw)
            fCSF.write(p)

        if sStringType == "WRTS":
            sString2Value = dCSF[sStringKey]["String2Value"]
            iString2ValueLength = len(sString2Value)
            p = struct.pack("<L%ds" % iString2ValueLength, iString2ValueLength, bytes(sString2Value, encoding='ascii'))
            fCSF.write(p)