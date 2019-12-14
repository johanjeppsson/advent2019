import math
import re
from collections import defaultdict

from utils import get_data


class Factory:
    def __init__(self, recipes):
        self._parse_recipes(recipes)

    def _parse_recipes(self, recipes):
        self.recipes = {}
        self.quantities = {}

        element_re = re.compile(r"(\d+)\s+(\w+)")
        for line in recipes.splitlines():
            elements = element_re.findall(line)
            inputs = elements[:-1]
            output = elements[-1]
            self.recipes[output[1]] = tuple(((int(i[0]), i[1]) for i in inputs))
            self.quantities[output[1]] = int(output[0])
        self.quantities["ORE"] = 1

    def fuel_requirement(self, fuel):
        requirements = defaultdict(int)
        requirements["FUEL"] = fuel
        surplus = defaultdict(int)
        ore_cnt = 0
        while len(requirements) > 0:
            new_req = defaultdict(int)
            for e, q in requirements.items():
                needed = q - surplus[e]
                m = math.ceil(needed / self.quantities[e])
                surplus[e] = (m * self.quantities[e]) - needed
                if e == "ORE":
                    ore_cnt += needed
                    continue
                for quan, comp in self.recipes[e]:
                    new_req[comp] += m * quan
            requirements = new_req
        return ore_cnt

    def binary_search(self, target):
        L = math.ceil(target / self.fuel_requirement(1))
        R = L * 2
        while L < (R - 1):
            m = (L + R) // 2
            f = self.fuel_requirement(m)
            if f < target:
                L = min(m + 1, R - 1)
            elif f > target:
                R = max(m - 1, L + 1)
            else:
                return int(m)
        if self.fuel_requirement(R) > target:
            return int(L)
        return int(R)


if __name__ == "__main__":
    f = Factory(get_data())
    print(f"Requirement for 1 fuel: {f.fuel_requirement(1)}")

    target = int(1e12)
    print(f"Fuel from {target} ore: {f.binary_search(target)}")
