from brian import (NeuronGroup, Network, StateMonitor,
                   second, ms, volt, mV)
import numpy as np
import matplotlib.pyplot as plt

network = Network()
XT = -50*mV
DeltaT = 0.05*mV/ms
eqs = "dX/dt = DeltaT*exp((X-XT)/DeltaT) : volt"

neuron = NeuronGroup(1, eqs, threshold="X>=XT", reset=-65*mV)
neuron.X = -65*mV
network.add(neuron)

vmon = StateMonitor(neuron, "X", record=True)
network.add(vmon)

network.run(1*second)

plt.figure("Voltage")
plt.plot(vmon.times, vmon[0])
plt.show()
