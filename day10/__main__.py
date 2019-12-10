import math

import numpy as np
from tqdm import tqdm

from utils import get_data


class AstMap:
    def __init__(self, ast_map):
        self.rows = [list(r) for r in ast_map.strip().split("\n")]
        self.n_x = len(self.rows[0])
        self.n_y = len(self.rows)

        self.coords, self.visible = self.find_best()

    def __str__(self):
        print("\n".join(["".join(r) for f in self.rows]))

    def set(self, x, y, val):
        self.rows[y][x] = val

    def get(self, x, y):
        return self.rows[y][x]

    def has_ast(self, x, y):
        return self.get(x, y) == "#"

    def find_best(self):
        best_match = {}
        best_coords = (0, 0)
        for x in tqdm(range(self.n_x)):
            for y in range(self.n_y):
                if not self.has_ast(x, y):
                    continue
                matches = self.eval_pos(x, y)
                if len(matches) > len(best_match):
                    best_match = matches
                    best_coords = (x, y)
        return best_coords, best_match

    def eval_pos(self, x, y):
        matches = {}
        for sx in range(self.n_x):
            for sy in range(self.n_y):
                if sx == x and sy == y:
                    continue
                if not self.has_ast(sx, sy):
                    continue
                dx = sx - x
                dy = y - sy
                r = math.sqrt(dx ** 2 + dy ** 2)
                phi = math.atan2(dx, dy)
                if dx < 0:
                    phi += 2 * math.pi
                if phi not in matches or r < matches[phi]["dist"]:
                    matches[phi] = {"dist": r, "coord": (sx, sy)}
        return matches

    def blast(self, n=1):
        phi_list = sorted(self.visible.keys())
        for i in range(n):
            phi = phi_list[i]
            x, y = self.visible[phi]["coord"]
            self.set(x, y, ".")
        self.visible = self.eval_pos(self.coords[0], self.coords[1])
        return x, y


if __name__ == "__main__":
    ast_map = AstMap(get_data())
    print(f"Best pos at {ast_map.coords} with {len(ast_map.visible)} astroids")

    ast_200 = ast_map.blast(200)
    print(f"200th astroid {ast_200}: {100*ast_200[0] + ast_200[1]}")
