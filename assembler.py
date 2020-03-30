instructions = {
    #   instr        tp   opcode             f3     f7
        'add'     : ('R', int('0110011', 2),   0x0,   0x00),
        'sub'     : ('R', int('0110011', 2),   0x0,   0x20),
        'xor'     : ('R', int('0110011', 2),   0x4,   0x00),
        'or'      : ('R', int('0110011', 2),   0x6,   0x00),
        'and'     : ('R', int('0110011', 2),   0x7,   0x00),
        'sll'     : ('R', int('0110011', 2),   0x1,   0x00),
        'srl'     : ('R', int('0110011', 2),   0x5,   0x00),
        'sra'     : ('R', int('0110011', 2),   0x5,   0x20),
        'slt'     : ('R', int('0110011', 2),   0x2,   0x00),
        'addi'    : ('I', int('0010011', 2),   0x0)        ,
        'xori'    : ('I', int('0010011', 2),   0x4)        ,
        'ori'     : ('I', int('0010011', 2),   0x6)        ,
        'andi'    : ('I', int('0010011', 2),   0x7)        ,
        'slli'    : ('I', int('0010011', 2),   0x1)        ,
        'srli'    : ('I', int('0010011', 2),   0x5)        ,
        'srai'    : ('I', int('0010011', 2),   0x5)        ,
        'slti'    : ('I', int('0010011', 2),   0x2)        ,
        'sltiu'   : ('I', int('0010011', 2),   0x3)        ,
        'lb'      : ('I', int('0000011', 2),   0x0)        ,
        'lh'      : ('I', int('0000011', 2),   0x1)        ,
        'lw'      : ('I', int('0000011', 2),   0x2)        ,
        'lbu'     : ('I', int('0000011', 2),   0x4)        ,
        'lhu'     : ('I', int('0000011', 2),   0x5)        ,
        'sb'      : ('S', int('0100011', 2),   0x0)        ,
        'sh'      : ('S', int('0100011', 2),   0x1)        ,
        'sw'      : ('S', int('0100011', 2),   0x2)        ,
        'beq'     : ('B', int('1100011', 2),   0x0)        ,
        'bne'     : ('B', int('1100011', 2),   0x1)        ,
        'blt'     : ('B', int('1100011', 2),   0x4)        ,
        'bge'     : ('B', int('1100011', 2),   0x5)        ,
        'bltu'    : ('B', int('1100011', 2),   0x6)        ,
        'bgeu'    : ('B', int('1100011', 2),   0x7)        ,
        'jal'     : ('J', int('1101111', 2))               ,
        'jalr'    : ('I', int('1100111', 2),   0x0)        ,
        'lui'     : ('U', int('0110111', 2))               ,
        'auipc'   : ('U', int('0010111', 2))               ,
        'ecall'   : ('I', int('1110011', 2),   0x0)        ,
        'ebreak'  : ('I', int('1110011', 2),   0x0)
}

def encode_instruction(instr):
    components = get_components(instr)
    print(components)
    info = instructions[components[0]]
    typ = info[0]
    if typ == 'R':
        instr, rd, rs1, rs2 = components
        _, opcode, f3, f7 = info
        rd_i = int(rd[1:])
        rs1_i = int(rs1[1:])
        rs2_i = int(rs2[1:])

        print('instr: {}'.format(instr))
        print('rd: {}, rd_i = {}'.format(rd, rd_i))
        print('rs1: {}, rs1_i = {}'.format(rs1, rs1_i))
        print('rs2: {}, rs2_i = {}'.format(rs2, rs2_i))
        print('f3: {:b}'.format(f3))
        print('f7: {:b}'.format(f7))

        return encode_rtype(opcode, rd_i, f3, rs1_i, rs2_i, f7)

    elif typ == 'I':
        instr, rd, rs1, imm = components
        _, opcode, f3 = info
        rd_i = int(rd[1:])
        rs1_i = int(rs1[1:])
        imm_b = twos_complement_str(int(imm), 12)
        imm_i = int(imm)

        print('instr: {}'.format(instr))
        print('rd: {}, rd_i = {}'.format(rd, rd_i))
        print('rs1: {}, rs1_i = {}'.format(rs1, rs1_i))
        print('imm: {}'.format(imm))
        print('f3: {0:b}'.format(f3))

        return encode_itype(opcode, rd_i, f3, rs1_i, imm_i)

    elif typ == 'S':
        instr, rs1, imm, rs2 = components
        _, opcode, f3 = info
        rs1_i = int(rs1[1:])
        rs2_i = int(rs2[1:])
        imm_i = int(imm)


        return encode_stype(opcode, f3, rs1_i, rs2_i, imm_i)

    elif typ == 'B':
        print('TODO')
    elif typ == 'J':
        print('TODO')
    elif typ == 'U':
        print('TODO')
    else:
        print('ERROR: unsupported instruction type ' + typ)

def twos_complement_str(x, width):
    if x & (1 << (width - 1)) == 1:
        return bin(x ^ ((1 << width) - 1) + 1)[2:]
    return bin(x)[2:]

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
               | ((imm_hi7 & 0x7f) << 25)

def main():
    i = input()
    encoded = encode_instruction(i)
    print(hex(encoded))

if __name__ == "__main__":
    main()


