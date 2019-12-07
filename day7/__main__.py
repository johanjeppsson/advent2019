from itertools import permutations

from utils import get_data
from utils.intcode import IntCode


class AmpCircuit:
    def __init__(self, prog, phases):
        self.amps = tuple(IntCode(prog) for i in range(5))
        self.phases = phases
        for ph, amp in zip(self.phases, self.amps):
            amp.run(ph, wait_for_input=True)

    def thrust(self, sig):
        for amp in self.amps:
            sig = amp.run(sig, wait_for_input=True)[0]
        return sig

    @property
    def halted(self):
        return all([a.halted for a in self.amps])


def max_thrust(prog, phases):
    best_thrust = 0
    best_phase = []
    for phase_config in permutations(phases):
        circ = AmpCircuit(prog, phase_config)
        thrust = 0
        while not circ.halted:
            thrust = circ.thrust(thrust)
        if thrust > best_thrust:
            best_thrust = thrust
            best_phase = phase_config
    return best_thrust, best_phase


prog = list(map(int, get_data(test=False).split(",")))

max_t, phase = max_thrust(prog, tuple(range(5)))
print(f"Max thruster (phase {phase}): {max_t}")

max_t_feedback, phase = max_thrust(prog, tuple(range(5, 10)))
print(f"Max thruster with feedback (phase: {phase}): {max_t_feedback}")
