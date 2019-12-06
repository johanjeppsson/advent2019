import networkx as nx
from matplotlib import pyplot as plt
from tqdm import tqdm

from utils import get_data


class obj:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    @property
    def nbr_orbits(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.nbr_orbits

    @property
    def parent_list(self):
        if self.parent is None:
            return [self]
        parent_list = self.parent.parent_list
        parent_list.insert(0, self)
        return parent_list

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


def plot_orb_graph(objects):
    edges = []
    for obj in objects.values():
        if obj.parent is not None:
            edges.append((obj.parent.name, obj.name))
    G = nx.DiGraph()
    G.add_edges_from(edges)
    pos = nx.spectral_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=10)
    nx.draw_networkx_edges(G, pos, arrows=False, alpha=0.4)
    plt.show()


data = get_data()

objects = {}
for orbit in tqdm(data.split(), desc="Creating orbits"):
    parent_name, child_name = orbit.split(")")
    if parent_name not in objects:
        parent = obj(parent_name, None)
        objects[parent_name] = parent
    if child_name in objects:
        objects[child_name].parent = objects[parent_name]
    else:
        child = obj(child_name, objects[parent_name])
        objects[child_name] = child
# plot_orb_graph(objects)

print(f"Checksum: {sum([o.nbr_orbits for o in objects.values()])}")

# Find common parent of YOU and SAN. The number of jumps is equal to the
san_par = objects["SAN"].parent.parent_list
you_par = objects["YOU"].parent.parent_list
for par in you_par:
    if par in san_par:
        break
print(f"Orbital jumps: {san_par.index(par) + you_par.index(par)}")
