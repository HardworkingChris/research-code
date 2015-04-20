"""
Reproduction of LIFwPR results.
"""
import brian_no_units
from brian import (Network, NeuronGroup, SpikeMonitor, StateMonitor,
                   PoissonGroup, Connection, network_operation,
                   mV, second, Hz, ms,
                   defaultclock, clear)
import matplotlib.pyplot as plt
import numpy as np
import spikerlib as sl
import multiprocessing as mp
import gc


def runsim(fin):
    clear(True)
    gc.collect()
    defaultclock.reinit()
    weight = 0.16*mV
    sim = Network()
    duration = 2.0*second
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
    return outisi, mnpss


frequencies = np.arange(100, 400, 1)
frequencies = np.reshape(frequencies, (10, 30))
pool = mp.Pool()
mppool = [pool.apply_async(runsim, [f]) for f in frequencies]
results = [res.get() for res in mppool]
outisi = []
mnpss = []
for res in results:
    outisi.extend(res[0])
    mnpss.extend(res[1])

outisi = np.array(outisi)
mnpss = np.array(mnpss)
sortidx = np.argsort(outisi)
outisi = outisi[sortidx]
mnpss = mnpss[sortidx]

plt.plot(outisi, mnpss, 'b.', marker=".", markersize=10)
plt.xlabel("$\overline{\mathrm{ISI}}$ (ms)")
plt.ylabel("$\overline{\mathrm{M}}$")
plt.axis(xmin=0, xmax=20, ymin=0)
xticks, _ = plt.xticks()
plt.xticks(np.append(xticks, 2))
plt.grid()
plt.savefig("npss_lifwpr.png")
plt.savefig("npss_lifwpr.pdf")
plt.show()
