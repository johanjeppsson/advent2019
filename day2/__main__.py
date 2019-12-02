from utils import get_data

HALT = 99
ADD = 1
MUL = 2

data = get_data()
prog = list(map(int, data.split(",")))

# Restore gravity assist
prog[1] = 12
prog[2] = 2


def calc(prog):
    idx = 0
    prog = prog.copy()
    while True:
        op = prog[idx]
        if op == HALT:
            return prog
        in1, in2, out = prog[idx + 1 : idx + 4]

        if op == ADD:
            prog[out] = prog[in1] + prog[in2]
        elif op == MUL:
            prog[out] = prog[in1] * prog[in2]
        idx += 4


print(f"Res at idx 0: {calc(prog)[0]}")

targ = 19690720
for noun in range(100):
    for verb in range(100):
        prog[1] = noun
        prog[2] = verb
        res = calc(prog)[0]
        if res == targ:
            print(
                f"Found match for noun {noun} and verb {verb}. Res: {100*noun + verb}"
            )
            break
