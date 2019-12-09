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
RLI = 9

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
    RLI: "REL IDX",
}

# Instruction lengths
N_PARAMS = {
    HLT: 0,
    ADD: 3,
    MUL: 3,
    INP: 1,
    OUT: 1,
    JPT: 2,
    JPF: 2,
    LTH: 3,
    EQU: 3,
    RLI: 1,
}

# Modes
POS = 0
IMM = 1
REL = 2

MODE_NAMES = {POS: "POS", IMM: "IMM", REL: "REL"}


class IntCode:
    def __init__(self, prog, dbg=False):
        if type(prog) != list:
            prog = list(map(int, prog.split(",")))
        self.prog = prog.copy()
        self.ram = self.prog.copy()
        self.idx = 0
        self.rel_idx = 0
        self.dbg = dbg
        self.halted = False
        self.op_cnt = 0

        self.print(f"Read program: {self.prog}")

    def run(self, inp=[], wait_for_input=False, dbg=False):
        if type(inp) == int:
            inp = [inp]

        out = []
        while True:
            inst, modes = self.get_op()
            self.print(
                f"op: {self.op_cnt:3} - idx: {self.idx:3d}, rel_idx: {self.rel_idx:3d}: {self.ram[self.idx]:5} "
                f"inst: {inst} {INST_NAMES[inst].ljust(max(map(len, INST_NAMES.values())))}"
                f" modes: {list(MODE_NAMES[m] for m in modes)}"
            )

            if inst == HLT:
                self.print("")
                self.halted = True
                return out

            inst_idxs = []
            params = []
            for i in range(N_PARAMS[inst]):
                inst_idx = self.gpi(1 + i, modes[i])
                if inst_idx >= len(self.ram):
                    self.ram.extend([0] * (1 + inst_idx - len(self.ram)))
                    self.print("Extended memory")
                inst_idxs.append(inst_idx)
                params.append(self.ram[inst_idx])

            self.print(
                f"       - params: {list(self.ram[self.idx + i + 1] for i in range(N_PARAMS[inst]))}"
                f" inst idx: {inst_idxs} "
                f"param vals: {params}\n"
            )
            self.op_cnt += 1

            if inst == ADD:
                self.ram[inst_idxs[2]] = params[0] + params[1]
            elif inst == MUL:
                self.ram[inst_idxs[2]] = params[0] * params[1]
            elif inst == INP:
                if len(inp) > 0:
                    self.ram[inst_idxs[0]] = inp.pop(0)
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
                self.ram[inst_idxs[2]] = int(params[0] < params[1])
            elif inst == EQU:
                self.ram[inst_idxs[2]] = int(params[0] == params[1])
            elif inst == RLI:
                self.rel_idx += params[0]
            else:
                raise ValueError(f"Invalid instruction: {inst}")
            self.idx += N_PARAMS[inst] + 1

    def get_op(self):
        op = self.ram[self.idx]
        inst = op % 100
        modes = []
        for i in range(N_PARAMS[inst]):
            modes.append((op // (10 ** (2 + i))) % 10)
        return inst, modes

    def gpi(self, off, mode):
        """Get parameter idx."""
        if mode == POS:
            return self.ram[self.idx + off]
        elif mode == IMM:
            return self.idx + off
        elif mode == REL:
            return self.ram[self.idx + off] + self.rel_idx
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def print(self, s):
        if self.dbg:
            print(s)
