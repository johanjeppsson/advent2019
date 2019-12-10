import math

from utils import get_data

from .__main__ import AstMap

map1 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

map5 = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""


def test_ast_map():
    am = AstMap(map1)

    assert am.n_x == 10
    assert am.n_y == 10

    assert am.get(0, 0) == "."
    assert not am.has_ast(0, 0)

    assert am.get(0, 1) == "#"
    assert am.has_ast(0, 1)


def test_eval_pos():

    am = AstMap("""#...#""")
    matches = am.eval_pos(4, 0)
    assert len(matches) == 1
    assert (3 * math.pi / 2) in matches
    assert matches[3 * math.pi / 2]["dist"] == 4
    assert matches[3 * math.pi / 2]["coord"] == (0, 0)

    matches = am.eval_pos(0, 0)
    assert len(matches) == 1
    assert math.pi / 2 in matches
    assert matches[math.pi / 2]["dist"] == 4
    assert matches[math.pi / 2]["coord"] == (4, 0)

    am = AstMap("""#.#.#""")
    matches = am.eval_pos(0, 0)
    assert len(matches) == 1
    assert math.pi / 2 in matches
    assert matches[math.pi / 2]["dist"] == 2
    assert matches[math.pi / 2]["coord"] == (2, 0)


def test_map1():
    am = AstMap(map1)
    assert am.coords == (5, 8)
    assert len(am.visible) == 33


def test_map2():
    map2 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
    am = AstMap(map2)

    assert am.coords == (1, 2)
    assert len(am.visible) == 35


def test_map3():
    map3 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
    am = AstMap(map3)

    assert am.coords == (6, 3)
    assert len(am.visible) == 41


def test_map4():
    map4 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    am = AstMap(map4)

    assert am.coords == (11, 13)
    assert len(am.visible) == 210

    ast_1 = am.blast(1)
    assert ast_1 == (11, 12)

    am = AstMap(map4)
    ast_200 = am.blast(200)
    assert ast_200 == (8, 2)


def test_map5():
    am = AstMap(map5)

    assert am.coords == (8, 3)

    ast_1 = am.blast(1)
    assert ast_1 == (8, 1)

    am = AstMap(map5)
    ast_9 = am.blast(9)
    assert ast_9 == (15, 1)
