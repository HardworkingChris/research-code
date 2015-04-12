"""
Reproduction of main results.
"""
from brian import (Network, NeuronGroup, SpikeMonitor, StateMonitor,
                   Connection, defaultclock, clear,
                   mV, second, Hz, ms)
import gc
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
import itertools as itt
import spikerlib as sl


def runsim(Nin, weight, fout, sync):
    sim = Network()
    clear(True)
    gc.collect()
    defaultclock.reinit()
    duration = 2*second
    lifeq = "dV/dt = -V/(10*ms) : volt"
    nrndef = {"model": lifeq, "threshold": "V>=15*mV", "reset": "V=0*mV",
              "refractory": 2*ms}
    print("Calibrating {} {} {}".format(Nin, weight, fout))
    fin = sl.tools.calibrate_frequencies(nrndef, Nin, weight, syncconf, fout,
                                         Vth=15*mV, tau=10*ms)
    inputgroups = []
    connections = []
    neurons = []
    voltagemons = []
    spikemons = []
    for fin_i, (sync_i, sigma_i) in zip(fin, syncconf):
        neuron = NeuronGroup(len(fin), **nrndef)
        inputgrp = sl.tools.fast_synchronous_input_gen(Nin, fin_i,
                                                       sync_i, sigma_i,
                                                       duration)
        defaultclock.reinit()
        neurons.append(neuron)
        conn = Connection(inputgrp, neuron, state="V", weight=weight)
        vmon = StateMonitor(neuron, "V", record=True)
        spikemon = SpikeMonitor(neuron, record=True)
        inputgroups.append(inputgrp)
        connections.append(conn)
        voltagemons.append(vmon)
        spikemons.append(spikemon)
    sim.add(*neurons)
    sim.add(*inputgroups)
    sim.add(*connections)
    sim.add(*voltagemons)
    sim.add(*spikemons)
    print("Running {} {} {}".format(Nin, weight, fout))
    sim.run(duration, report="stdout")
    mnpss = []
    for vmon, smon, sync in zip(voltagemons, spikemons, syncconf):
        if smon.nspikes:
            npss = sl.tools.npss(vmon[0], smon[0], 0*mV, 15*mV, 10*ms, 2*ms)
            if np.any(npss > 100):
                break
        else:
            npss = 0
        mnpss.append(np.mean(npss))
    imshape = (len(sigma), len(Sin))
    imextent = (0, 1, 0, 4.0)
    mnpss = np.reshape(mnpss, imshape, order="F")
    plt.figure()
    plt.imshow(mnpss, aspect="auto", origin="lower", extent=imextent,
               vmin=0, vmax=1)
    cbar = plt.colorbar()
    cbar.set_label("$\overline{M}$")
    plt.xlabel("$S_{in}$")
    plt.ylabel("$\sigma_{in}$ (ms)")
    filename = "npss_{}_{}_{}".format(Nin, weight, fout).replace(".", "")
    plt.savefig(filename+".pdf")
    plt.savefig(filename+".png")
    print("{} saved".format(filename))


Nin = [100, 50, 60, 60, 200, 60]
weight = [0.1*mV, 0.2*mV, 0.3*mV, 0.5*mV, 0.1*mV, 0.5*mV]
fout = [5*Hz, 100*Hz, 10*Hz, 70*Hz, 10*Hz, 100*Hz]
Sin = np.arange(0, 1.01, 0.1)
sigma = np.arange(0, 4.1, 0.5)*ms
syncconf = [(s, j) for s, j in itt.product(Sin, sigma)]

configurations = []
for n, w, f in zip(Nin, weight, fout):
    configurations.append({"Nin": n, "weight": w, "fout": f, "sync": syncconf})

pool = mp.Pool()
print("Building pool")
mppool = [pool.apply_async(runsim, kwds=c) for c in configurations]
print("Getting results")
results = [res.get() for res in mppool]
