# Instructions
HLT = 99
ADD = 1
MUL = 2
INP = 3
OUT = 4
JPT = 5
JPF = 6
LTH = 7
EQU = 8

# Nice names
INST_NAMES = {
    HLT: "HALT",
    ADD: "ADD",
    MUL: "MUL",
    INP: "INPUT",
    OUT: "OUTPUT",
    JPT: "JUMP IF TRUE",
    JPF: "JUMP IF FALSE",
    LTH: "LESS THAN",
    EQU: "EQUALS",
}

# Instruction lengths
N_PARAMS = {HLT: 0, ADD: 3, MUL: 3, INP: 1, OUT: 1, JPT: 2, JPF: 2, LTH: 3, EQU: 3}

# Modes
POS = 0
IMM = 1


def parse_op(op):
    inst = op % 100
    modes = []
    for i in range(N_PARAMS[inst]):
        modes.append((op // (10 ** (2 + i))) % 10)
    return inst, modes


def gpi(prog, idx, mode):
    """Get parameter idx."""
    if mode == POS:
        return prog[idx]
    elif mode == IMM:
        return idx
    else:
        raise ValueError(f"Unknown mode: {mode}")


def d_print(s, dbg):
    if dbg:
        print(s)


def run_prog(prog, inp=[], dbg=False):
    if type(inp) == int:
        inp = [inp]
    idx = 0
    while True:
        inst, modes = parse_op(prog[idx])

        d_str = (
            f"ptr: {idx}: {prog[idx]} inst: {inst}, {INST_NAMES[inst]} modes: {modes}"
        )

        if inst == HLT:
            d_print(d_str, dbg)
            d_print("", dbg)
            break

        params = []
        for i in range(N_PARAMS[inst]):
            params.append(prog[gpi(prog, idx + 1 + i, modes[i])])

        d_str += f" params: {params}"
        d_print(d_str, dbg)

        if inst == ADD:
            prog[gpi(prog, idx + N_PARAMS[inst], 0)] = params[0] + params[1]
        elif inst == MUL:
            prog[gpi(prog, idx + N_PARAMS[inst], 0)] = params[0] * params[1]
        elif inst == INP:
            prog[gpi(prog, idx + N_PARAMS[inst], 0)] = inp.pop(0)
        elif inst == OUT:
            yield params[0]
        elif inst == JPT:
            if params[0] != 0:
                idx = params[1]
                continue
        elif inst == JPF:
            if params[0] == 0:
                idx = params[1]
                continue
        elif inst == LTH:
            prog[gpi(prog, idx + 3, 0)] = int(params[0] < params[1])
        elif inst == EQU:
            prog[gpi(prog, idx + 3, 0)] = int(params[0] == params[1])
        else:
            raise ValueError(f"Invalid instruction: {inst}")
        idx += N_PARAMS[inst] + 1
