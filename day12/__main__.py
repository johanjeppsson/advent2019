import re
from dataclasses import dataclass, replace

from utils import get_data


@dataclass
class Coord:

    x: int
    y: int
    z: int

    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon:
    def __init__(self, name, pos, vel):
        self.name = name
        self.pos = Coord(*pos)
        self.vel = Coord(*vel)

        self.start_pos = replace(self.pos)
        self.start_vel = replace(self.vel)

    @classmethod
    def from_spec(cls, spec, name="Moon"):
        m = re.match(r"<x=([^,]*), y=([^,]*), z=([^,]*)>", spec)
        return Moon(name, map(int, m.groups()), [0] * 3)

    def __str__(self):
        return f"{self.name}: pos={self.pos} vel={self.vel}"

    def __repr__(self):
        return self.__str__()

    def reset(self):
        self.pos = replace(self.start_pos)
        self.vel = replace(self.start_vel)

    def sign(self, v):
        return (v > 0) - (v < 0)

    def update_vel(self, other):
        self.vel.x += self.sign(other.pos.x - self.pos.x)
        self.vel.y += self.sign(other.pos.y - self.pos.y)
        self.vel.z += self.sign(other.pos.z - self.pos.z)

    def update_pos(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def energy(self):
        return self.pos.abs_sum() * self.vel.abs_sum()


class System:
    def __init__(self, specs):
        self.moons = []
        for i, spec in enumerate(specs.strip().split("\n")):
            self.moons.append(Moon.from_spec(spec, "Moon{}".format(i + 1)))

    def tick(self, ticks=1):
        for i in range(ticks):
            for moon in self.moons:
                for other in self.moons:
                    moon.update_vel(other)
            for moon in self.moons:
                moon.update_pos()

    def energy(self):
        return sum([m.energy() for m in self.moons])

    def reset(self):
        for m in self.moons:
            m.reset()

    def get_coords(self, axis="x"):
        return tuple((getattr(m.pos, axis) for m in self.moons))

    def get_vels(self, axis="x"):
        return tuple((getattr(m.vel, axis) for m in self.moons))

    def ax_period(self, axis="x"):
        start_coords = self.get_coords(axis)
        start_vels = self.get_vels(axis)

        self.tick()

        period = 1
        while (
            self.get_coords(axis) != start_coords or self.get_vels(axis) != start_vels
        ):
            self.tick()
            period += 1
        return period

    def lcm(self, a, b):
        g = max(a, b)
        l = min(a, b)
        m = g
        while m % l:
            m += g
        return m

    def period(self):
        x_period = self.ax_period("x")
        print(f"x: {x_period}")
        self.reset()

        y_period = self.ax_period("y")
        print(f"y: {y_period}")
        self.reset()

        z_period = self.ax_period("z")
        print(f"z: {z_period}")
        self.reset()

        return self.lcm(self.lcm(x_period, y_period), z_period)

        greatest = max(max(x_period, y_period), z_period)
        period = greatest
        while (period % x_period) or (period % y_period) or (period % z_period):
            period += greatest
        return period


if __name__ == "__main__":
    data = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
    s = System(get_data())
    # s = System(data)
    s.tick(1000)
    print(f"Energy after 1000 steps: {s.energy()}")

    s.reset()
    print(f"System period: {s.period()}")
