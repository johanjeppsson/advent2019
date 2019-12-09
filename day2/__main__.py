from utils import get_data
from utils.intcode import IntCode


def run(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb

    p = IntCode(prog)
    out = p.run()
    return p.ram[0]


if __name__ == "__main__":
    data = get_data()
    prog = list(map(int, data.split(",")))

    print(f"Res at idx 0: {run(prog, 12, 2)}")

    targ = 19690720
    for noun in range(100):
        for verb in range(100):
            res = run(prog, noun, verb)
            if res == targ:
                print(
                    f"Found match for noun {noun} and verb {verb}. Res: {100*noun + verb}"
                )
                break
