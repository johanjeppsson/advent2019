from .__main__ import Moon, System


def test_ex1():

    specs = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    system = System(specs)
    system.tick(1)

    assert system.moons[0].vel.x == 3
    assert system.moons[0].vel.y == -1
    assert system.moons[0].vel.z == -1
    assert system.moons[0].pos.x == 2
    assert system.moons[0].pos.y == -1
    assert system.moons[0].pos.z == 1

    system.tick(9)
    assert system.moons[0].vel.x == -3
    assert system.moons[0].vel.y == -2
    assert system.moons[0].vel.z == 1
    assert system.moons[0].pos.x == 2
    assert system.moons[0].pos.y == 1
    assert system.moons[0].pos.z == -3

    assert system.energy() == 179


if __name__ == "__main__":
    test_ex1()
