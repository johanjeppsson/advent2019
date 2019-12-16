import random
from collections import defaultdict

import numpy as np
from matplotlib import pyplot as plt

from utils import get_data, get_key
from utils.intcode import IntCode

from .a_star import a_star, path_to_rel_moves

plt.ion()


class Maze:

    UNKNOWN = 0
    PATH = 1
    OXYGEN = 2
    WALL = 3
    ROBOT = 4

    MOVE_DICT = {(-1, 0): 1, (1, 0): 2, (0, -1): 3, (0, 1): 4}

    def __init__(self, code, plot=True):
        self.prog = IntCode(code)

        self.x = 0
        self.y = 0
        self.maze = np.zeros((3, 3), dtype=np.uint8)
        self.oxy_x = None
        self.oxy_y = None

        self.mark(self.x, self.y, self.PATH)

        if plot:
            self.disp = np.zeros(
                (self.maze.shape[0], self.maze.shape[1], 3), dtype=np.uint8
            )
            self.plot = plt.imshow(self.disp)
            self.update_plot()
            self.updating = False

    def coord(self, y, x):
        x_out = x + self.maze.shape[1] // 2
        y_out = y + self.maze.shape[0] // 2

        while (x_out < 0 or x_out >= self.maze.shape[1]) or (
            y_out < 0 or y_out >= self.maze.shape[0]
        ):
            self.pad()
            x_out = x + self.maze.shape[1] // 2
            y_out = y + self.maze.shape[0] // 2

        return y_out, x_out

    def mark(self, y, x, val):
        cy, cx = self.coord(y, x)
        self.maze[cy, cx] = val

    def pad(self):
        self.maze = np.pad(self.maze, 1)
        if hasattr(self, "disp"):
            self.disp = np.pad(self.disp, ((1, 1), (1, 1), (0, 0)))

    def move(self, dy=0, dx=0):
        assert abs(dx) + abs(dy) < 2
        res = self.prog.run(self.MOVE_DICT[(dy, dx)], wait_for_input=True)[0]
        if res == 0:
            # We hit a wall
            self.mark(self.y + dy, self.x + dx, self.WALL)
        elif res == 1 or res == 2:
            # We moved to a path tile
            self.x += dx
            self.y += dy
            self.mark(self.y, self.x, self.PATH)
        if res == 2:
            # We moved to the oxygen source tile
            self.oxy_x = self.x
            self.oxy_y = self.y

        if hasattr(self, "plot"):
            self.update_plot()

        return res == 1 or res == 2

    def update_plot(self):
        self.disp[...] = 0
        r_idx = np.where((self.maze == self.WALL) | (self.maze == self.PATH))
        r_idx = tuple((*r_idx, np.ones_like(r_idx) * 0))

        self.disp[r_idx] = 255

        g_idx = np.where((self.maze == self.PATH) | (self.maze == self.ROBOT))
        g_idx = tuple((*g_idx, np.ones_like(g_idx) * 1))
        self.disp[g_idx] = 255

        b_idx = np.where((self.maze == self.PATH) | (self.maze == self.OXYGEN))
        b_idx = tuple((*b_idx, np.ones_like(b_idx) * 2))
        self.disp[b_idx] = 255

        ry, rx = self.coord(self.y, self.x)
        self.disp[ry, rx, :] = [0, 255, 0]
        if self.oxy_x is not None:
            oy, ox = self.coord(self.oxy_y, self.oxy_x)
            self.disp[ry, rx, :] = [0, 0, 255]

        self.plot.set_data(self.disp)
        plt.draw()
        plt.pause(0.01)

    def handle_keypress(self, event):
        coords = [0, 0]
        if event.key == "q":
            plt.gcf().canvas.mpl_disconnect(self.key_cid)
            plt.ion()
            return
        elif event.key == "up":
            coords[0] = -1
        elif event.key == "down":
            coords[0] = 1
        elif event.key == "right":
            coords[1] = 1
        elif event.key == "left":
            coords[1] = -1
        else:
            return
        self.move(*coords)

    def manual(self):
        self.key_cid = plt.gcf().canvas.mpl_connect(
            "key_press_event", self.handle_keypress
        )
        plt.ioff()
        plt.show()
        print(self.maze.shape)

    def unknown_neighbors(self):
        unknown = []
        for dy, dx in self.MOVE_DICT.keys():
            cy, cx = self.coord(self.y + dy, self.x + dx)
            if self.maze[cy, cx] == self.UNKNOWN:
                unknown.append((dy, dx))
        return unknown if unknown else None

    def random(self):
        while np.any(self.maze == self.UNKNOWN):
            try:
                n = self.unknown_neighbors()[0]
                if n is not None:
                    dy, dx = n
                else:
                    dy, dx = random.choice(list(self.MOVE_DICT.keys()))
                self.move(dy, dx)
            except KeyboardInterrupt:
                break
        print(self.maze.shape)

    def astar(self):
        while True:
            un = self.unknown_neighbors()
            if un is not None:
                success_d = None
                for n in un:
                    if self.move(*n):
                        success_d = n
                        self.move(-n[0], -n[1])
                self.move(*success_d)
                continue
            cy, cx = self.coord(self.y, self.x)
            possible_targets = zip(*np.where(self.maze == 0))
            paths = [
                a_star((self.maze > 2).astype(int), (cy, cx), t)
                for t in possible_targets
            ]
            paths = [path_to_rel_moves(p) if p is not None else None for p in paths]
            if not paths or all([p is None for p in paths]):
                break
            path_lengths = [len(p) if p is not None else np.inf for p in paths]
            shortest = paths[path_lengths.index(min(path_lengths))]
            for move in shortest:
                self.move(*move)


if __name__ == "__main__":

    m = Maze(get_data(), plot=True)
    m.astar()
    plt.show()
    plt.pause(3)
