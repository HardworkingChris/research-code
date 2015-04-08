from brian import (Network, NeuronGroup, StateMonitor,
                   mV, ms)
import spikerlib as sl

sim = Network()
tau = 10*ms
Vth = 15*mV
Vreset = 0*mV
lifeq = "dV/dt = -V/tau : volt"

lifnrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset=Vreset)
lifnrn.V = Vreset
sim.add(lifnrn)

vmon = StateMonitor(lifnrn, "V", record=True)
sim.add(vmon)

