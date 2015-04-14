"""
Reproduction of LIFwPR results.
"""
from brian import (Network, NeuronGroup, SpikeMonitor, StateMonitor,
                   PoissonGroup, Connection, network_operation,
                   mV, second, Hz, ms)
import matplotlib.pyplot as plt
import numpy as np
import spikerlib as sl


fin = np.arange(100, 401, 10)
weight = 0.16*mV
sim = Network()
duration = 5*second
Vth = 15*mV
Vreset = 13.65*mV
trefr = 2*ms
lifeq = """
dV/dt = -V/(10*ms) : volt
Vth : volt
"""
nrndef = {"model": lifeq, "threshold": "V>=Vth", "reset": "V=Vreset",
          "refractory": 0.1*ms}
inputgroups = []
connections = []
neurons = []
Nneurons = len(fin)
neurons = NeuronGroup(Nneurons, **nrndef)
neurons.V = 0*mV
neurons.Vth = 15*mV
for idx in range(Nneurons):
    fin_i = fin[idx]*Hz
    inputgrp = PoissonGroup(50, fin_i)
    conn = Connection(inputgrp, neurons[idx], state="V", weight=weight)
    inputgroups.append(inputgrp)
    connections.append(conn)
voltagemon = StateMonitor(neurons, "V", record=True)
spikemon = SpikeMonitor(neurons, record=True)
sim.add(neurons, voltagemon, spikemon)
sim.add(*inputgroups)
sim.add(*connections)

@network_operation
def refractory_threshold(clock):
    for idx in range(Nneurons):
        if (len(spikemon.spiketimes[idx])
                and clock.t < spikemon.spiketimes[idx][-1]*second+trefr):
            neurons.Vth[idx] = 100*mV
        else:
            neurons.Vth[idx] = Vth

sim.add(refractory_threshold)
print("Running simulation of {} neurons for {} s".format(Nneurons, duration))
sim.run(duration, report="stdout")

mnpss = []
allnpss = []
outisi = []
for idx in range(Nneurons):
    vmon = voltagemon[idx]
    smon = spikemon[idx]
    if not len(smon):
        continue
    outisi.append(duration*1000/len(smon))
    if len(smon) > 0:
        npss = sl.tools.npss(vmon, smon, 0*mV, 15*mV, 10*ms, 2*ms)
    else:
        npss = 0
    mnpss.append(np.mean(npss))
    allnpss.append(npss)

plt.plot(outisi, mnpss, 'b--', marker=".", markersize=10)
plt.xlabel("$\overline{ISI}$ (ms)")
plt.ylabel("$\overline{M}$")
plt.axis(xmin=0, xmax=20, ymin=0)
plt.savefig("npss_lifwpr.png")
plt.savefig("npss_lifwpr.pdf")
plt.show()
