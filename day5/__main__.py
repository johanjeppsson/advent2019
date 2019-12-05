from utils import get_data
from utils.intcode import run_prog

data = get_data()
prog = list(map(int, data.split(",")))

AC_ID = 1
DIAG_ID = 5

for out in run_prog(prog.copy(), AC_ID):
    print(out)

for out in run_prog(prog.copy(), DIAG_ID):
    print(out)
