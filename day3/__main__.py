from tqdm import tqdm

from utils import get_data

data = get_data()
w1_spec = data.split("\n")[0]
w2_spec = data.split("\n")[1]

w1 = {}
w2 = {}

DX = {"L": -1, "R": 1}
DY = {"U": -1, "D": 1}


def create_wire(spec):
    x = 0
    y = 0
    tot_l = 0
    wire = {}
    for line in tqdm(spec.split(",")):
        direction = line[0]
        length = int(line[1:])
        for _ in range(length):
            wire[(x, y)] = tot_l
            tot_l += 1
            x += DX.get(direction, 0)
            y += DY.get(direction, 0)
    return wire


w1 = create_wire(w1_spec)
w2 = create_wire(w2_spec)

intersections = set(w1.keys()).intersection(set(w2.keys()))
intersections.remove((0, 0))

closest = None
shortest = None
for i in intersections:
    dist = abs(i[0]) + abs(i[1])
    length = w1[i] + w2[i]
    if closest is None or dist < closest:
        closest = dist
    if shortest is None or length < shortest:
        shortest = length

print(f"Closest intersection: {closest}")
print(f"Shortest intersection: {shortest}")
