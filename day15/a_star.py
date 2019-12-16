from collections import defaultdict

import numpy as np


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def assemble_path(came_from, target):
    path = [target]
    while path[0] in came_from:
        path.insert(0, came_from[path[0]])

    return path


def path_to_mask(m, path):
    mask = np.zeros_like(m)
    idx = ([p[0] for p in path], [p[1] for p in path])
    mask[idx] = 1
    return mask


def path_to_rel_moves(path):
    rel_moves = []
    for i in range(len(path) - 1):
        dy = path[i + 1][0] - path[i][0]
        dx = path[i + 1][1] - path[i][1]
        rel_moves.append((dy, dx))
    return rel_moves


def a_star(m, start, target, h=heuristic):
    neighbors = ((-1, 0), (1, 0), (0, -1), (0, 1))

    open_set = set()
    open_set.add(start)
    closed_set = set()
    came_from = {}

    g_score = defaultdict(lambda: np.inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: np.inf)
    f_score[start] = h(start, target)

    while open_set:
        current = None
        for coord in open_set:
            if current is None or f_score[coord] < f_score[current]:
                current = coord

        if current == target:
            return assemble_path(came_from, target)

        open_set.remove(current)
        closed_set.add(current)
        for off_y, off_x in neighbors:
            neighbor = (current[0] + off_y, current[1] + off_x)
            if (neighbor[0] < 0 or neighbor[0] >= m.shape[0]) or (
                neighbor[1] < 0 or neighbor[1] >= m.shape[1]
            ):
                # Neighbor outside map
                continue
            if neighbor in closed_set:
                # Neighbor already evaluated
                continue
            if m[neighbor] == 1:
                # Neighbor is wall
                continue
            tenative_g_score = g_score[current] + h(current, neighbor)
            if tenative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tenative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor, target)
                open_set.add(neighbor)
    return None


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    m = np.array(
        [
            [0, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 1, 1],
            [0, 1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
        ]
    )

    path = a_star(m, (0, 0), (4, 6))
    mask = path_to_mask(m, path)
    img = m.copy()
    img += mask * 2
    plt.subplot(121)
    plt.imshow(m, vmax=2)
    plt.subplot(122)
    plt.imshow(img)
    plt.show()
