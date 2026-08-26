#!/usr/bin/env python3
import struct, sys, os, glob

popcap_to_lua51_op = {
    0: (0, "iABC"),   # OP_MOVE
    1: (1, "iABx"),   # OP_LOADK
    2: (2, "iABC"),   # OP_LOADBOOL
    3: (3, "iABC"),   # OP_LOADNIL
    4: (4, "iABC"),   # OP_GETUPVAL
    5: (5, "iABx"),   # OP_GETGLOBAL
    6: (6, "iABC"),   # OP_GETTABLE
    7: (7, "iABx"),   # OP_SETGLOBAL
    8: (8, "iABC"),   # OP_SETUPVAL
    9: (9, "iABC"),   # OP_SETTABLE
    10: (10, "iABC"), # OP_NEWTABLE
    11: (11, "iABC"), # OP_SELF
    12: (12, "iABC"), # OP_ADD
    13: (13, "iABC"), # OP_SUB
    14: (14, "iABC"), # OP_MUL
    15: (15, "iABC"), # OP_DIV
    16: (16, "iABC"), # OP_MOD
    17: (17, "iABC"), # OP_POW
    18: (18, "iABC"), # OP_UNM
    19: (19, "iABC"), # OP_NOT
    20: (20, "iABC"), # OP_LEN
    21: (21, "iABC"), # OP_CONCAT
    22: (22, "iAsBx"),# OP_JMP
    23: (23, "iABC"), # OP_EQ
    24: (24, "iABC"), # OP_LT
    25: (25, "iABC"), # OP_LE
    26: (26, "iABC"), # OP_TEST
    27: (28, "iABC"), # OP_CALL
    28: (29, "iABC"), # OP_TAILCALL
    29: (30, "iABC"), # OP_RETURN
    30: (31, "iAsBx"),# OP_FORLOOP
    31: (33, "iABC"), # OP_TFORLOOP
    32: (22, "iAsBx"),# OP_TFORPREP -> Lua 5.1 OP_JMP (22)
    33: (34, "iABC"), # OP_SETLIST
    34: (34, "iABC"), # OP_SETLISTO
    35: (35, "iABC"), # OP_CLOSE
    36: (11, "iABC"), # OP_ALTSELF
    37: (7, "iABx"),  # OP_CONSTGLOBAL
    38: (9, "iABC"),  # OP_CONSTTABLE
    39: (7, "iABx"),  # OP_DEFGLOBAL
    40: (9, "iABC"),  # OP_DEFTABLE
    41: (7, "iABx"),  # OP_SETSELFORGLOBAL
    42: (5, "iABx"),  # OP_GETSELFORGLOBAL
    43: (11, "iABC"), # OP_SELFORGLOBAL
    44: (28, "iABC"), # OP_CALLSELFORGLOBAL
    45: (29, "iABC"), # OP_TAILCALLSELFORGLOBAL
    46: (37, "iABC"), # OP_VARARG
    48: (36, "iABx"), # OP_CLOSURE
}

lua51_opmodes = {
    0:  (2, 0), # MOVE (R, N)
    1:  (0, 0), # LOADK (K, N)
    2:  (1, 1), # LOADBOOL (U, U)
    3:  (2, 0), # LOADNIL (R, N)
    4:  (1, 0), # GETUPVAL (U, N)
    5:  (0, 0), # GETGLOBAL (K, N)
    6:  (2, 3), # GETTABLE (R, K)
    7:  (0, 0), # SETGLOBAL (K, N)
    8:  (1, 0), # SETUPVAL (U, N)
    9:  (3, 3), # SETTABLE (K, K)
    10: (1, 1), # NEWTABLE (U, U)
    11: (2, 3), # SELF (R, K)
    12: (3, 3), # ADD (K, K)
    13: (3, 3), # SUB (K, K)
    14: (3, 3), # MUL (K, K)
    15: (3, 3), # DIV (K, K)
    16: (3, 3), # MOD (K, K)
    17: (3, 3), # POW (K, K)
    18: (2, 0), # UNM (R, N)
    19: (2, 0), # NOT (R, N)
    20: (2, 0), # LEN (R, N)
    21: (2, 2), # CONCAT (R, R)
    22: (0, 0), # JMP (R, N)
    23: (3, 3), # EQ (K, K)
    24: (3, 3), # LT (K, K)
    25: (3, 3), # LE (K, K)
    26: (0, 1), # TEST (N, U)
    27: (2, 1), # TESTSET (R, U)
    28: (1, 1), # CALL (U, U)
    29: (1, 1), # TAILCALL (U, U)
    30: (1, 0), # RETURN (U, N)
    31: (0, 0), # FORLOOP (R, N)
    32: (0, 0), # FORPREP (R, N)
    33: (0, 1), # TFORLOOP (N, U)
    34: (1, 1), # SETLIST (U, U)
    35: (0, 0), # CLOSE (N, N)
    36: (0, 0), # CLOSURE (U, N)
    37: (1, 0), # VARARG (U, N)
}

def convert_rk50(r):
    if r >= 250:
        k = r - 250
        return 256 + k
    return r

def convert_instruction(ins):
    raw_op = ins & 0x3F
    a = (ins >> 24) & 0xFF
    c = (ins >> 6) & 0x1FF
    b = (ins >> 15) & 0x1FF
    bx = (ins >> 6) & 0x3FFFF

    if raw_op not in popcap_to_lua51_op:
        raise ValueError(f"Unknown raw opcode: {raw_op}")

    std_op, mode = popcap_to_lua51_op[raw_op]

    if std_op == 34: # SETLIST
        std_b = c
        std_c = b + 1
        return (std_op & 0x3F) | ((a & 0xFF) << 6) | ((std_c & 0x1FF) << 14) | ((std_b & 0x1FF) << 23)

    if mode in ("iABx", "iAsBx"):
        return (std_op & 0x3F) | ((a & 0xFF) << 6) | ((bx & 0x3FFFF) << 14)
    else:
        b_mode, c_mode = lua51_opmodes.get(std_op, (0, 0))
        b_std = convert_rk50(b) if b_mode == 3 else b
        c_std = convert_rk50(c) if c_mode == 3 else c
        return (std_op & 0x3F) | ((a & 0xFF) << 6) | ((c_std & 0x1FF) << 14) | ((b_std & 0x1FF) << 23)

def convert_file(in_path, out_path):
    with open(in_path, "rb") as f:
        data = f.read()

    pos = 23
    def read_bytes(n):
        nonlocal pos; b = data[pos:pos+n]; pos += n; return b
    def read_int(): return struct.unpack("<i", read_bytes(4))[0]
    def read_uint(): return struct.unpack("<I", read_bytes(4))[0]
    def read_double(): return struct.unpack("<d", read_bytes(8))[0]
    def read_byte(): return read_bytes(1)[0]
    def read_string():
        size = read_uint()
        if size == 0: return ""
        return read_bytes(size)[:-1].decode("utf-8", errors="replace")

    def parse_proto():
        src = read_string()
        line_def = read_int()
        proto_id = read_int()
        nups = read_byte()
        numparams = read_byte()
        is_vararg = read_byte()
        maxstacksize = read_byte()

        sizelineinfo = read_int()
        lineinfo = [read_int() for _ in range(sizelineinfo)]

        sizelocvars = read_int()
        locvars = []
        for _ in range(sizelocvars):
            vname = read_string()
            spc = read_int()
            epc = read_int()
            locvars.append((vname, spc, epc))

        sizeupvalues = read_int()
        upvalues = [read_string() for _ in range(sizeupvalues)]

        sizek = read_int()
        constants = []
        for i in range(sizek):
            t = read_byte()
            if t == 0: val = (0, None)
            elif t == 1: val = (1, read_byte() != 0)
            elif t == 3: val = (3, read_double())
            elif t == 4: val = (3, float(read_int()))
            elif t == 5: val = (4, read_string())
            else: raise ValueError(f"Unknown const type {t}")
            constants.append(val)

        sizep = read_int()
        subprotos = [parse_proto() for _ in range(sizep)]
        sizecode = read_int()
        code = [convert_instruction(read_uint()) for _ in range(sizecode)]

        # Patch FORPREP for numeric for loops
        for pc, ins in enumerate(code):
            op = ins & 0x3F
            if op == 31: # OP_FORLOOP
                a = (ins >> 6) & 0xFF
                bx = (ins >> 14) & 0x3FFFF
                sbc = bx - 131071
                target_pc = pc + sbc
                if 0 <= target_pc < len(code):
                    forprep_sbx = pc - target_pc - 1
                    forprep_bx = forprep_sbx + 131071
                    code[target_pc] = (32 & 0x3F) | ((a & 0xFF) << 6) | ((forprep_bx & 0x3FFFF) << 14)

        return {
            "src": src,
            "line_def": line_def,
            "last_line_def": max(lineinfo) if lineinfo else line_def,
            "nups": nups,
            "numparams": numparams,
            "is_vararg": is_vararg,
            "maxstacksize": maxstacksize,
            "code": code,
            "constants": constants,
            "subprotos": subprotos,
            "lineinfo": lineinfo,
            "locvars": locvars,
            "upvalues": upvalues,
        }

    tree = parse_proto()

    out = bytearray()
    out.extend(b"\x1bLua\x51\x00\x01\x04\x08\x04\x08\x00")

    def write_int(v): out.extend(struct.pack("<i", v))
    def write_uint(v): out.extend(struct.pack("<I", v))
    def write_size_t(v): out.extend(struct.pack("<Q", v))
    def write_double(v): out.extend(struct.pack("<d", v))
    def write_byte(v): out.append(v & 0xFF)
    def write_string(s):
        if s is None:
            write_size_t(0)
        else:
            b = s.encode("utf-8") + b"\x00"
            write_size_t(len(b))
            out.extend(b)

    def serialize(p):
        write_string(p["src"])
        write_int(p["line_def"])
        write_int(p["last_line_def"])
        write_byte(p["nups"])
        write_byte(p["numparams"])
        write_byte(p["is_vararg"])
        write_byte(p["maxstacksize"])

        write_int(len(p["code"]))
        for ins in p["code"]:
            write_uint(ins)

        write_int(len(p["constants"]))
        for tag, val in p["constants"]:
            write_byte(tag)
            if tag == 0: pass
            elif tag == 1: write_byte(1 if val else 0)
            elif tag == 3: write_double(val)
            elif tag == 4: write_string(val)

        write_int(len(p["subprotos"]))
        for sub in p["subprotos"]:
            serialize(sub)

        write_int(0)

        write_int(len(p["locvars"]))
        for vname, spc, epc in p["locvars"]:
            write_string(vname)
            write_int(spc)
            write_int(epc)

        write_int(len(p["upvalues"]))
        for u in p["upvalues"]:
            write_string(u)

    serialize(tree)

    with open(out_path, "wb") as f:
        f.write(out)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 popcap_converter.py <input.luc> <output.luac>")
        sys.exit(1)
    convert_file(sys.argv[1], sys.argv[2])
