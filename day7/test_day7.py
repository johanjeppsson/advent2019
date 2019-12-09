from utils import get_data

from .__main__ import AmpCircuit, max_thrust


def test_day7():
    prog = list(map(int, get_data(__file__, test=False).split(",")))

    max_t, phase = max_thrust(prog, tuple(range(5)))
    assert phase == (1, 0, 2, 4, 3)
    assert max_t == 46248

    max_t_feedback, phase = max_thrust(prog, tuple(range(5, 10)))
    assert phase == (6, 8, 5, 9, 7)
    assert max_t_feedback == 54163586
