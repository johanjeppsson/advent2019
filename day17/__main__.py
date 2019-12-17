import numpy as np
from scipy.signal import convolve2d

from utils import get_data
from utils.intcode import IntCode


def to_ascii(i):
    return str(chr(i))


def to_np(cam_feed):
    cam_out = "".join(map(to_ascii, cam_feed))
    raw = np.vstack([np.array([c for c in l]) for l in cam_out.strip().splitlines()])
    return raw


def scaffold_mask(raw):
    # Translate to numbers
    out = np.zeros(raw.shape, dtype=int)
    out[np.where(raw == "#")] = 1
    out[np.where(raw == "<")] = 1
    out[np.where(raw == "^")] = 1
    out[np.where(raw == ">")] = 1
    out[np.where(raw == "v")] = 1
    return out


def find_repeats(s, sub, start=0):
    idxs = []
    while s.find(sub, start) > -1:
        idxs.append(s.find(sub, start))
        start = idxs[-1] + 1
    return idxs


def find_segment(s):
    matched_chars = 0
    best_sub = ""
    start = 0
    for i in range(3, 21):
        sub = s[:i]
        m = find_repeats(s, sub)
        if len(m) * i > matched_chars:
            matched_chars = len(m) * i
            best_sub = sub
    return best_sub


def find_path(raw):
    d = 0
    rc = np.where((raw == "^") | (raw == "v") | (raw == ">") | (raw == "<"))
    y = rc[0][0]
    x = rc[1][0]
    if "^" in raw:
        d = 0
    if "<" in raw:
        d = 1
    if "v" in raw:
        d = 2
    if ">" in raw:
        d = 3
    d_map = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}

    def next():
        dy, dx = d_map[d]
        return y + dy, x + dx

    scaffold = np.pad(scaffold_mask(raw), 1)
    x += 1
    y += 1
    instructions = []
    while 1 in scaffold:
        move_cnt = 0
        while scaffold[next()] != 1:
            d = (d + 1) % 4
            instructions.append("L")
        while scaffold[next()] > 0:
            move_cnt += 1
            scaffold[y, x] = 2
            y, x = next()
        scaffold[y, x] = 2
        instructions.append(str(move_cnt))

    inst_str = ",".join(instructions)
    inst_str = inst_str.replace("L,L,L", "R")

    A = find_segment(inst_str)
    B = find_segment(inst_str.replace(A, ""))
    C = find_segment(inst_str.replace(A, "").replace(B, ""))

    sequence = inst_str.replace(A, "A").replace(B, "B").replace(C, "C").replace(",", "")

    ret = {
        "sequence": ",".join(sequence),
        "A": A.rstrip(","),
        "B": B.rstrip(","),
        "C": C.rstrip(","),
    }
    return ret


if __name__ == "__main__":
    cam_feed = IntCode(get_data()).run()
    print("".join(map(to_ascii, cam_feed)))
    cam_feed = to_np(cam_feed)
    scaffold = scaffold_mask(cam_feed)

    kernel = np.array([[0, 0.2, 0], [0.2, 0.2, 0.2], [0, 0.2, 0]])
    intersect = list(zip(*np.where(convolve2d(scaffold, kernel, "same") == 1)))
    print(f"Checksum: {sum([i[0]*i[1] for i in intersect])}")

    path = find_path(cam_feed)

    robot = IntCode(get_data())
    robot.prog[0] = 2
    robot.ram[0] = 2

    s_in = list(map(ord, path["sequence"] + "\n"))
    a_in = list(map(ord, path["A"] + "\n"))
    b_in = list(map(ord, path["B"] + "\n"))
    c_in = list(map(ord, path["C"] + "\n"))
    f_in = list(map(ord, "n\n"))
    inputs = [[], s_in, a_in, b_in, c_in, f_in]
    for inp in inputs:
        print("".join(map(to_ascii, inp)))
        out = robot.run(inp[:], wait_for_input=True)
        print("".join(map(to_ascii, out)))

    print(f"Dust collected: {out[-1]}")
