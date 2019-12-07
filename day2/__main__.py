from utils import get_data
from utils.intcode import IntCode

HALT = 99
ADD = 1
MUL = 2

data = get_data()
prog = list(map(int, data.split(",")))

# Restore gravity assist
prog[1] = 12
prog[2] = 2

p = IntCode(prog)
for out in p.run():
    print(out)

print(f"Res at idx 0: {p.prog[0]}")

targ = 19690720
for noun in range(100):
    for verb in range(100):
        prog[1] = noun
        prog[2] = verb

        p = IntCode(prog)
        for out in p.run():
            print(out)
        res = p.prog[0]
        if res == targ:
            print(
                f"Found match for noun {noun} and verb {verb}. Res: {100*noun + verb}"
            )
            break
