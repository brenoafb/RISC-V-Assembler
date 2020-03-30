INSTRUCTIONS = {
    #   instr        tp   opcode             f3     f7
        'add'     : ('R', int('0110011', 2), 0x0, 0x00),
        'sub'     : ('R', int('0110011', 2), 0x0, 0x20),
        'xor'     : ('R', int('0110011', 2), 0x4, 0x00),
        'or'      : ('R', int('0110011', 2), 0x6, 0x00),
        'and'     : ('R', int('0110011', 2), 0x7, 0x00),
        'sll'     : ('R', int('0110011', 2), 0x1, 0x00),
        'srl'     : ('R', int('0110011', 2), 0x5, 0x00),
        'sra'     : ('R', int('0110011', 2), 0x5, 0x20),
        'slt'     : ('R', int('0110011', 2), 0x2, 0x00),
        'addi'    : ('I', int('0010011', 2), 0x0),
        'xori'    : ('I', int('0010011', 2), 0x4),
        'ori'     : ('I', int('0010011', 2), 0x6),
        'andi'    : ('I', int('0010011', 2), 0x7),
        'slli'    : ('I', int('0010011', 2), 0x1),
        'srli'    : ('I', int('0010011', 2), 0x5),
        'srai'    : ('I', int('0010011', 2), 0x5),
        'slti'    : ('I', int('0010011', 2), 0x2),
        'sltiu'   : ('I', int('0010011', 2), 0x3),
        'lb'      : ('I', int('0000011', 2), 0x0),
        'lh'      : ('I', int('0000011', 2), 0x1),
        'lw'      : ('I', int('0000011', 2), 0x2),
        'lbu'     : ('I', int('0000011', 2), 0x4),
        'lhu'     : ('I', int('0000011', 2), 0x5),
        'sb'      : ('S', int('0100011', 2), 0x0),
        'sh'      : ('S', int('0100011', 2), 0x1),
        'sw'      : ('S', int('0100011', 2), 0x2),
        'beq'     : ('B', int('1100011', 2), 0x0),
        'bne'     : ('B', int('1100011', 2), 0x1),
        'blt'     : ('B', int('1100011', 2), 0x4),
        'bge'     : ('B', int('1100011', 2), 0x5),
        'bltu'    : ('B', int('1100011', 2), 0x6),
        'bgeu'    : ('B', int('1100011', 2), 0x7),
        'jal'     : ('J', int('1101111', 2)),
        'jalr'    : ('I', int('1100111', 2), 0x0),
        'lui'     : ('U', int('0110111', 2)),
        'auipc'   : ('U', int('0010111', 2)),
        'ecall'   : ('I', int('1110011', 2), 0x0),
        'ebreak'  : ('I', int('1110011', 2), 0x0)
}

def encode_instruction(instr):
    print()
    print(instr)
    components = get_components(instr)
    print(components)
    info = INSTRUCTIONS[components[0]]
    typ = info[0]
    if typ == 'R':
        op, rd, rs1, rs2 = components
        _, opcode, f3, f7 = info
        rd_i = int(rd[1:])
        rs1_i = int(rs1[1:])
        rs2_i = int(rs2[1:])

        print('op: {}'.format(op))
        print('rd: {}, rd_i = {}'.format(rd, rd_i))
        print('rs1: {}, rs1_i = {}'.format(rs1, rs1_i))
        print('rs2: {}, rs2_i = {}'.format(rs2, rs2_i))
        print('f3: {:b}'.format(f3))
        print('f7: {:b}'.format(f7))

        return encode_rtype(opcode, rd_i, f3, rs1_i, rs2_i, f7)

    if typ == 'I':
        op = components[0]
        if is_load(op):
            _, rd, imm, rs1 = components
        else:
            _, rd, rs1, imm = components

        _, opcode, f3 = info
        rd_i = int(rd[1:])
        rs1_i = int(rs1[1:])
        imm_i = int(imm)

        print('op: {}'.format(op))
        print('rd: {}, rd_i = {}'.format(rd, rd_i))
        print('rs1: {}, rs1_i = {}'.format(rs1, rs1_i))
        print('imm: {}'.format(imm))
        print('f3: {0:b}'.format(f3))

        return encode_itype(opcode, rd_i, f3, rs1_i, imm_i)

    if typ == 'S':
        op, rs2, imm, rs1 = components
        _, opcode, f3 = info
        rs1_i = int(rs1[1:])
        rs2_i = int(rs2[1:])
        imm_i = int(imm)

        print('op: {}'.format(op))
        print('rs1: {}, rs1_i = {}'.format(rs1, rs1_i))
        print('rs2: {}, rs2_i = {}'.format(rs2, rs2_i))
        print('imm: {}'.format(imm))
        print('f3: {0:b}'.format(f3))

        return encode_stype(opcode, f3, rs1_i, rs2_i, imm_i)

    if typ == 'B':
        op, rs1, rs2, imm = components
        _, opcode, f3 = info

        rs1_i = int(rs1[1:])
        rs2_i = int(rs2[1:])
        imm_i = int(imm)

        print('op: {}'.format(op))
        print('rs1: {}, rs1_i = {}'.format(rs1, rs1_i))
        print('rs2: {}, rs2_i = {}'.format(rs2, rs2_i))
        print('imm: {}'.format(imm))
        print('f3: {0:b}'.format(f3))

        return encode_btype(opcode, f3, rs1_i, rs2_i, imm_i)

    if typ == 'J':
        op, rd, imm = components

        rd_i = int(rs1[1:])
        imm_i = int(imm)

        print('op: {}'.format(op))
        print('rd: {}, rd_i = {}'.format(rd, rd_i))
        print('imm: {}'.format(imm))


        return encode_jtype(opcode, rd_i, imm_i)
    if typ == 'U':
        op, rd, imm = components
        _, opcode = info

        rd_i = int(rs1[1:])
        imm_i = int(imm)

        print('op: {}'.format(op))
        print('rd: {}, rd_i = {}'.format(rd, rd_i))
        print('imm: {}'.format(imm))

        return encode_utype(opcode, rd_i, imm_i)

    print('ERROR: unsupported instruction type ' + typ)

def get_components(instr):
    return instr.replace('(', ' ').replace(')', ' ').replace(',', '').split()

def encode_rtype(opcode, rd, f3, rs1, rs2, f7):
    return ((opcode & 0x7f)
            | ((rd & 0x1f)  << 7)
            | ((f3 & 0x7)   << 12)
            | ((rs1 & 0x1f) << 15)
            | ((rs2 & 0x1f) << 20)
            | ((f7 & 0x7f)  << 25))


def encode_itype(opcode, rd, f3, rs1, imm):
   return ((opcode & 0x7f)
           | ((rd & 0x1f)   << 7)
           | ((f3 & 0x7)    << 12)
           | ((rs1 & 0x1f)  << 15)
           | ((imm & 0xfff) << 20))


def encode_stype(opcode, f3, rs1, rs2, imm):
    imm_lo5 = imm & 0x1f
    imm_hi7 = (imm >> 5) & 0x7f
    return ((opcode & 0x7f)
            | ((imm_lo5 & 0x1f) << 7)
            | ((f3 & 0x7) << 12)
            | ((rs1 & 0x1f) << 15)
            | ((rs2 & 0x1f) << 20)
            | ((imm_hi7 & 0x7f) << 25))

def encode_btype(opcode, f3, rs1, rs2, imm):
    imm_1_4 = (imm >> 1) & 0x7
    imm_5_10 = (imm >> 5) & 0xf
    imm_11 = (imm >> 11) & 0x1
    imm_12 = (imm >> 12) & 0x1

    return ((opcode & 0x7f)
            | (imm_11 << 7)
            | (imm_1_4 << 8)
            | ((f3 & 0x7) << 12)
            | ((rs1 & 0x7f) << 15)
            | ((rs2 & 0x7f) << 20)
            | (imm_5_10 << 25)
            | (imm_12 << 31))


def encode_utype(opcode, rd, imm):
    return ((opcode & 0x7f)
            | ((rd & 0x7f) << 7)
            | ((imm & 0xfffff) << 12))

def encode_jtype(opcode, rd, imm):
    imm_12_19 = (imm >> 12) & 0xff
    imm_1_10 = (imm >> 1) & 0x1ff
    imm_11 = (imm >> 11) & 0x1
    imm_20 = (imm >> 20) & 0x1
    return ((opcode & 0x7f)
            | ((rd & 0x7f) << 7)
            | (imm_12_19 << 12)
            | (imm_11 << 20)
            | (imm_1_10 << 21)
            | (imm_20 << 31))

def is_load(op):
    return op in ['lb', 'lh', 'lw', 'lbu', 'lhu']

def main():
    i = input()
    encoded = encode_instruction(i)
    print(hex(encoded))

# if __name__ == "__main__":
#     main()

def test():
    for (instr, expected) in TESTS.items():
        result = encode_instruction(instr)
        print('expected: {}, result: {}'.format(hex(expected), hex(result)))
        assert result == expected

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
