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


class IntCode:
    def __init__(self, prog, dbg=False):
        self.prog = prog.copy()
        self.idx = 0
        self.dbg = dbg
        self.halted = False

    def run(self, inp=[], wait_for_input=False, dbg=False):
        if type(inp) == int:
            inp = [inp]

        out = []
        while True:
            inst, modes = self.get_op()

            d_str = f"ptr: {self.idx}: {self.prog[self.idx]} inst: {inst}, {INST_NAMES[inst]} modes: {modes}"

            if inst == HLT:
                self.print(d_str)
                self.print("")
                self.halted = True
                return out

            params = []
            for i in range(N_PARAMS[inst]):
                params.append(self.prog[self.gpi(self.idx + 1 + i, modes[i])])

            d_str += f" params: {params}"
            self.print(d_str)

            if inst == ADD:
                self.prog[self.gpi(self.idx + N_PARAMS[inst], 0)] = (
                    params[0] + params[1]
                )
            elif inst == MUL:
                self.prog[self.gpi(self.idx + N_PARAMS[inst], 0)] = (
                    params[0] * params[1]
                )
            elif inst == INP:
                if len(inp) > 0:
                    self.prog[self.gpi(self.idx + N_PARAMS[inst], 0)] = inp.pop(0)
                elif wait_for_input:
                    # Halt program and wait for it to be called with more input
                    return out
                else:
                    raise RuntimeError("Expected input, but input list was empty")
            elif inst == OUT:
                out.append(params[0])
            elif inst == JPT:
                if params[0] != 0:
                    self.idx = params[1]
                    continue
            elif inst == JPF:
                if params[0] == 0:
                    self.idx = params[1]
                    continue
            elif inst == LTH:
                self.prog[self.gpi(self.idx + 3, 0)] = int(params[0] < params[1])
            elif inst == EQU:
                self.prog[self.gpi(self.idx + 3, 0)] = int(params[0] == params[1])
            else:
                raise ValueError(f"Invalid instruction: {inst}")
            self.idx += N_PARAMS[inst] + 1

    def get_op(self):
        op = self.prog[self.idx]
        inst = op % 100
        modes = []
        for i in range(N_PARAMS[inst]):
            modes.append((op // (10 ** (2 + i))) % 10)
        return inst, modes

    def gpi(self, idx, mode):
        """Get parameter idx."""
        if mode == POS:
            return self.prog[idx]
        elif mode == IMM:
            return idx
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def print(self, s):
        if self.dbg:
            print(s)
