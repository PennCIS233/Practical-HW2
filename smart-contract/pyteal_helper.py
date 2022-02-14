# adapted from https://github.com/algorand/pyteal-utils/blob/main/pytealutils/strings/string.py
from pyteal import (
    Assert,
    BitLen,
    Btoi,
    Bytes,
    BytesDiv,
    BytesGt,
    BytesMod,
    Concat,
    Extract,
    GetByte,
    If,
    Int,
    Itob,
    Len,
    ScratchVar,
    Seq,
    Subroutine,
    Substring,
    TealType,
)

@Subroutine(TealType.bytes)
def int_to_ascii(arg):
    """int_to_ascii converts an integer to the ascii byte that represents it"""
    return Extract(Bytes("0123456789"), arg, Int(1))

@Subroutine(TealType.bytes)
def itoa(i):
    """itoa converts an integer to the ascii byte string it represents"""
    return If(
        i == Int(0),
        Bytes("0"),
        Concat(
            If(i / Int(10) > Int(0), itoa(i / Int(10)), Bytes("")),
            int_to_ascii(i % Int(10)),
        ),
    )