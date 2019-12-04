from tqdm import tqdm

from utils import get_data

pw_min, pw_max = map(int, get_data().split("-"))


def validate(pw, allow_larger=False):
    double = False
    last = 10
    counts = {d: 0 for d in range(10)}
    for sh in range(6):
        digit = (pw // (10 ** sh)) % 10
        if digit > last:
            return False
        counts[digit] += 1
        last = digit
    if allow_larger:
        return max(counts.values()) >= 2
    return 2 in counts.values()


valid = 0
for pw in tqdm(range(pw_min, pw_max)):
    valid += int(validate(pw, allow_larger=True))
print(valid)

valid = 0
for pw in tqdm(range(pw_min, pw_max)):
    valid += int(validate(pw))
print(valid)
