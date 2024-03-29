import re
import sys
import termios
import tty
from pathlib import Path

import requests

import __main__


def get_data(file_name=None, test=False):
    """Get raw data string for the current day.
    Download from adventofcode.com if necessary, using the session cookie
    in the .cookie file.
    """
    if file_name is None:
        dir_name = Path(__main__.__file__).parent
    else:
        dir_name = Path(file_name).parent
    data_file = dir_name / "input.txt"
    if test:
        data_file = dir_name / "test_input.txt"

    # Use cached data if possible
    if data_file.exists():
        return data_file.open("r").read()
    elif test:
        raise ValueError(f"Could not find {data_file}")

    cookie = Path(".cookie")
    if not cookie.exists():
        raise ValueError("Save session cookie as .cookie in base dir")

    day = re.match(r"day(\d+)", dir_name.name).group(1)
    url = f"https://adventofcode.com/2019/day/{day}/input"

    r = requests.get(url, cookies={"session": cookie.open("r").read().strip()})

    data = r.text
    data_file.open("w").write(data)

    return data


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
