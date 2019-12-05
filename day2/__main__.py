from utils import get_data
from utils.intcode import run_prog

HALT = 99
ADD = 1
MUL = 2

data = get_data()
prog = list(map(int, data.split(",")))

# Restore gravity assist
prog[1] = 12
prog[2] = 2

prog_after = prog.copy()
for out in run_prog(prog_after, []):
    print(out)

print(f"Res at idx 0: {prog_after[0]}")

targ = 19690720
for noun in range(100):
    for verb in range(100):
        prog_after = prog.copy()
        prog_after[1] = noun
        prog_after[2] = verb

        for out in run_prog(prog_after, []):
            print(out)
        res = prog_after[0]
        if res == targ:
            print(
                f"Found match for noun {noun} and verb {verb}. Res: {100*noun + verb}"
            )
            break
