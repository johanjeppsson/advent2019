from utils import get_data

from .__main__ import run


def test_day2():
    prog = list(map(int, get_data(__file__).split(",")))
    assert run(prog, 12, 2) == 4090689

    assert run(prog, 77, 33) == 19690720
    assert run(prog, 77, 32) != 19690720
