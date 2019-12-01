with open('day1/data.txt', 'r') as f:
    data = list(map(int, f.readlines()))

def fuel_req(mass):
    return max((mass // 3) - 2, 0)

print("Fuel requirement without fuel: ", sum([fuel_req(m) for m in data]))

tot_fuel = 0
for m in data:
    fuel = fuel_req(m)
    tot_fuel += fuel
    while fuel > 0:
        fuel = fuel_req(fuel)
        tot_fuel += fuel

print("Fuel requirement with fuel: ", tot_fuel)
