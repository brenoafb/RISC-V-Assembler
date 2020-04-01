from assembler import encode_instruction

TESTS = {
    'add x10, x10, x11 ' : 0x00b50533,
    'add x12, x8, x13  ' : 0x00d40633,
    'add x30, x0, x20  ' : 0x01400f33,
    'sub x10, x10, x11 ' : 0x40b50533,
    'sub x12, x8, x13  ' : 0x40d40633,
    'sub x30, x0, x20  ' : 0x41400f33,
    'xor x10, x10, x11 ' : 0x00b54533,
    'xor x12, x8, x13  ' : 0x00d44633,
    'xor x30, x0, x20  ' : 0x01404f33,
    'or x10, x10, x11  ' : 0x00b56533,
    'or x12, x8, x13   ' : 0x00d46633,
    'or x30, x0, x20   ' : 0x01406f33,
    'and x10, x10, x11 ' : 0x00b57533,
    'and x12, x8, x13  ' : 0x00d47633,
    'and x30, x0, x20  ' : 0x01407f33,
    'sll x10, x10, x11 ' : 0x00b51533,
    'sll x12, x8, x13  ' : 0x00d41633,
    'sll x30, x0, x20  ' : 0x01401f33,
    'srl x10, x10, x11 ' : 0x00b55533,
    'srl x12, x8, x13  ' : 0x00d45633,
    'srl x30, x0, x20  ' : 0x01405f33,
    'sra x10, x10, x11 ' : 0x40b55533,
    'sra x12, x8, x13  ' : 0x40d45633,
    'sra x30, x0, x20  ' : 0x41405f33,
    'slt x10, x10, x11 ' : 0x00b52533,
    'slt x12, x8, x13  ' : 0x00d42633,
    'slt x30, x0, x20  ' : 0x01402f33,
    'addi x10, x10, 1  ' : 0x00150513,
    'addi x10, x12, 100' : 0x06460513,
    'addi x4, x4, 20   ' : 0x01420213,
    'addi x4, x1, -1   ' : 0xfff08213,
    'xori x10, x10, 1  ' : 0x00154513,
    'xori x10, x12, 100' : 0x06464513,
    'xori x4, x4, 20   ' : 0x01424213,
    'xori x4, x1, -1   ' : 0xfff0c213,
    'ori x10, x10, 1   ' : 0x00156513,
    'ori x10, x12, 100 ' : 0x06466513,
    'ori x4, x4, 20    ' : 0x01426213,
    'ori x4, x1, -1    ' : 0xfff0e213,
    'andi x10, x10, 1  ' : 0x00157513,
    'andi x10, x12, 100' : 0x06467513,
    'andi x4, x4, 20   ' : 0x01427213,
    'andi x4, x1, -1   ' : 0xfff0f213,
    'slli x10, x10, 1  ' : 0x00151513,
    'slli x10, x12, 3  ' : 0x00361513,
    'slli x4, x4, 8    ' : 0x00821213,
    'slli x4, x1, 1    ' : 0x00109213,
    'srli x10, x10, 1  ' : 0x00155513,
    'srli x10, x12, 2  ' : 0x00265513,
    'srli x4, x4, 12   ' : 0x00c25213,
    'srli x4, x1, 1    ' : 0x0010d213,
    'srai x10, x10, 1  ' : 0x40155513,
    'srai x10, x12, 12 ' : 0x40c65513,
    'srai x4, x4, 2    ' : 0x40225213,
    'srai x4, x1, 1    ' : 0x4010d213,
    'slti x10, x10, 1  ' : 0x00152513,
    'slti x10, x12, 1  ' : 0x00162513,
    'slti x4, x4, 2    ' : 0x00222213,
    'slti x4, x1, 1    ' : 0x0010a213,
    'sltiu x10, x10, 1 ' : 0x00153513,
    'sltiu x10, x12, 10' : 0x00a63513,
    'sltiu x4, x4, 2   ' : 0x00223213,
    'sltiu x4, x1, 1   ' : 0x0010b213,
    'lb x9, 0(x10)     ' : 0x00050483,
    'lb x8, 240(x10)   ' : 0x0f050403,
    'lb x8, 32(x10)    ' : 0x02050403,
    'lb x8, -1(x1)     ' : 0xfff08403,
    'lh x9, 0(x10)     ' : 0x00051483,
    'lh x8, 240(x10)   ' : 0x0f051403,
    'lh x8, 32(x10)    ' : 0x02051403,
    'lh x8, -1(x1)     ' : 0xfff09403,
    'lw x9, 0(x10)     ' : 0x00052483,
    'lw x8, 240(x10)   ' : 0x0f052403,
    'lw x8, 32(x10)    ' : 0x02052403,
    'lw x8, -1(x1)     ' : 0xfff0a403,
    'lbu x9, 0(x10)    ' : 0x00054483,
    'lbu x8, 240(x10)  ' : 0x0f054403,
    'lbu x8, 32(x10)   ' : 0x02054403,
    'lbu x8, -1(x1)    ' : 0xfff0c403,
    'lhu x9, 0(x10)    ' : 0x00055483,
    'lhu x8, 240(x10)  ' : 0x0f055403,
    'lhu x8, 32(x10)   ' : 0x02055403,
    'lhu x8, -1(x1)    ' : 0xfff0d403,
    'sb x9, 0(x10)     ' : 0x00950023,
    'sb x8, 240(x10)   ' : 0x0e850823,
    'sb x8, 32(x10)    ' : 0x02850023,
    'sb x8, -1(x1)     ' : 0xfe808fa3,
    'sh x9, 0(x10)     ' : 0x00951023,
    'sh x8, 240(x10)   ' : 0x0e851823,
    'sh x8, 32(x10)    ' : 0x02851023,
    'sh x8, -1(x1)     ' : 0xfe809fa3,
    'sw x9, 0(x10)     ' : 0x00952023,
    'sw x8, 240(x10)   ' : 0x0e852823,
    'sw x8, 32(x10)    ' : 0x02852023,
    'sw x8, -1(x1)     ' : 0xfe80afa3,
    }

def test():
    for (instr, expected) in TESTS.items():
        result = encode_instruction(instr)
        print('expected: {}, result: {}'.format(hex(expected), hex(result)))
        assert result == expected
    print('PASS')

if __name__ == '__main__':
    test()
