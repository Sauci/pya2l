def get_unpack_format_from_a2l_datatype(datatype: str) -> str:
    return dict(UBYTE='B',
                SBYTE='b',
                UWORD='H',
                SWORD='h',
                ULONG='I',
                SLONG='i',
                FLOAT32_IEEE='f',
                FLOAT64_IEEE='d')[datatype]


def get_byte_size_from_unpack_format(packing_format: str) -> int:
    result = 0
    for c in packing_format:
        if c.lower() == 'b':
            result += 1
        if c.lower() == 'h':
            result += 2
        if c.lower() == 'i':
            result += 4
        if c.lower() == 'f':
            result += 4
        if c.lower() == 'd':
            result += 8
    return result
