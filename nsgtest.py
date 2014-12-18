"""
Script for testing brian on NSG portal.
Still trying to figure out how it all works.
"""

from brian import (Network, NeuronGroup, StateMonitor, SpikeMonitor,
                   PoissonInput,
                   mV, ms, second, Hz)
import numpy as np

network = Network()

tau = 20*ms
eqs = "dV/dt = -V/tau : volt"
lifgroup = NeuronGroup(10, eqs, threshold="V>=(20*mV)", reset=0*mV)
weights = np.linspace(0.1, 1, 10)
rates = np.arange(10, 100, 10)
inputgroups = []
for idx, (w, r) in enumerate(zip(weights, rates)):
    inpgrp = PoissonInput(lifgroup[idx], 20, r*Hz, w*mV, state="V")
    inputgroups.append(inpgrp)
network.add(lifgroup)
network.add(*inputgroups)

spikemon = SpikeMonitor(lifgroup)
vmon = StateMonitor(lifgroup, "V", record=True)

network.add(spikemon, vmon)
network.run(10*second, report="stdout")

spikes = spikemon.spiketimes.values()
voltage = vmon.values
np.savez("results.npz",
         spikes=spikes,
         voltages=voltage)
print("DONE")
