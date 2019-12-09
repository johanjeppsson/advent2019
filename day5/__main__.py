from utils import get_data
from utils.intcode import IntCode

AC_ID = 1
DIAG_ID = 5

if __name__ == "__main__":
    data = get_data()
    prog = list(map(int, data.split(",")))

    p = IntCode(prog)
    for out in p.run(AC_ID):
        print(out)

    p = IntCode(prog)
    for out in p.run(DIAG_ID):
        print(out)
