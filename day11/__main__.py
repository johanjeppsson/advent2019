import numpy as np

from utils import get_data
from utils.intcode import IntCode

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DISP = {UP: "^", RIGHT: ">", LEFT: "<", DOWN: "v"}


class Robot:
    def __init__(self, prog):
        self.prog = prog
        self.painted = np.zeros((125, 125), dtype=int)
        self.color = np.zeros_like(self.painted)
        self.x = self.painted.shape[1] // 2
        self.y = self.painted.shape[0] // 2
        self.dir = 0

    def print(self):
        out_str = ""
        for y, row in enumerate(self.color):
            for x, color in enumerate(row):
                if x == self.x and y == self.y:
                    out_str += DISP[self.dir]
                    continue
                out_str += "#" if color == 1 else "."
            out_str += "\n"
        print(out_str)

    def paint(self, color):
        self.color[self.y, self.x] = color
        self.painted[self.y, self.x] += 1

    def move(self, direction):
        if direction == 1:
            self.dir += 1
        else:
            self.dir -= 1
        self.dir %= 4

        if self.dir == UP:
            self.y -= 1
        elif self.dir == RIGHT:
            self.x += 1
        elif self.dir == DOWN:
            self.y += 1
        elif self.dir == LEFT:
            self.x -= 1

    def step(self):
        inp = int(self.color[self.y, self.x])
        out = self.prog.run(inp, wait_for_input=True)
        if not out:
            return False
        self.paint(out[0])
        self.move(out[1])
        return True

    def run(self):
        running = True
        while running:
            running = self.step()


if __name__ == "__main__":
    prog = IntCode(get_data())
    r = Robot(prog)
    r.run()
    print(f"Start on black: Painted {np.count_nonzero(r.painted > 0)} tiles")

    prog = IntCode(get_data())
    r = Robot(prog)
    r.color[r.y, r.x] = 1
    r.run()
    print(f"Start on white: Painted {np.count_nonzero(r.painted > 0)} tiles")
    r.print()
