from utils import get_data
import numpy as np
from tqdm import tqdm, trange

def get_phases(inp):
    base = np.array([0, 1, 0 ,-1])
    bases = []
    for i in tqdm(range(len(inp)), desc="Calculating bases"):
        reps = int(np.ceil(inp.size / (base.size * (i + 1))))
        bases.append(np.roll(np.repeat(np.tile(base, reps), i + 1), -1)[:inp.size])
    return np.vstack(bases)

def FFT(inp, phases):
    out = []
    for i in range(len(inp)):
        out.append(inp * phases[i, :])
    out = np.abs(np.array(out).sum(1).T) % 10
    return out

def part1(inp, iters=100):
    phases = get_phases(inp)
    out = inp
    for i in trange(iters, desc="Iteration"):
        inp = FFT(inp, phases)
    return "".join(map(str, inp[:8]))

def part2(inp, offs, iters=100):
    # Using the approach from part1 in this case is _really_ slow and requires
    # a _lot_ of memory due to the large input /many phases.
    # Here, use that the offset is larger than N / 2, which means that all
    # coefficients are either 0 or 1, e.g. the lower right quarter of the
    # coefficients below:
    #
    #     1  2  3  4  5  6  7  8
    #   ------------------------
    # 1 | 1  0 -1  0  1  0 -1  0
    # 2 | 0  1  1  0  0 -1 -1  0
    # 3 | 0  0  1  1  1  0  0  0
    # 4 | 0  0  0  1  1  1  1  0
    # 5 | 0  0  0  0  1  1  1  1
    # 6 | 0  0  0  0  0  1  1  1
    # 7 | 0  0  0  0  0  0  1  1
    # 8 | 0  0  0  0  0  0  0  1
    #
    # This means that the coefficients for each position i, the output is the
    # sum from i to the end of the array. If we iterate backwards, that means
    # that each position is the sum of the output on the previous index and
    # the input of the current index, which is a cumulative sum. 
    N = inp.size
    out = inp.copy()
    assert(off > N // 2)
    for i in trange(iters, desc="Iteration"):
        out[offs:] = np.cumsum(inp[-1:offs-1:-1])[::-1] % 10
        inp = out
    return "".join(map(str, out[off:off+8]))


if __name__ == "__main__":
    data = get_data()
    inp = np.array(list(map(int, data.strip())))
    print(f"Part 1: {part1(inp)}")

    inp = np.array(list(map(int, data.strip())))
    inp = np.tile(inp, 10000)
    off = int(''.join(map(str, inp[:7])))
    print(f"Part 2: {part2(inp, off)}")
