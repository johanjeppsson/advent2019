from utils import get_data
from utils.intcode import IntCode

from .__main__ import AC_ID, DIAG_ID


def test_day5():
    prog = list(map(int, get_data(__file__).split(",")))
    p = IntCode(prog)
    out_ac = p.run(AC_ID)

    assert out_ac == [0, 0, 0, 0, 0, 0, 0, 0, 0, 13787043]

    p = IntCode(prog)
    out_diag = p.run(DIAG_ID)
    assert out_diag == [3892695]
