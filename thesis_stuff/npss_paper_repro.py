"""
Reproduction of main results.
"""
from brian import (Network, NeuronGroup, SpikeMonitor, StateMonitor,
                   Connection, defaultclock,
                   mV, second, Hz)
import numpy as np
import multiprocessing as mp
import itertools as itt
import spikerlib as sl


def runsim(Nin, weight, fout):
    sim = Network()
    defaultclock.reinit()
    duration = 5*second
    lifeq = "dV/dt = -V/(10*mV) : volt"
    Sin = np.arange(0, 1.01, 0.1)
    sigma = np.arange(0, 4.1, 0.5)
    nrndef = {"model": lifeq, "threshold": "V>=15*mV", "reset": "V=0*mV"}
    syncprod = itt.product(Sin, sigma)
    print("Calibrating {} {} {}".format(Nin, weight, fout))
    fin = sl.tools.calibrate_frequencies(nrndef, Nin, weight, fout)
    inputgroups = []
    connections = []
    neurons = []
    voltagemons = []
    spikemons = []
    for fin_i, (sync_i, sigma_i) in zip(fin, syncprod):
        neuron = NeuronGroup(len(fin), **nrndef)
        inputgrp = sl.tools.fast_synchronous_input_gen(Nin, fin_i,
                                                       sync_i, sigma_i,
                                                       duration)
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
    sim.add(*conn)
    sim.add(*voltagemons)
    sim.add(*spikemons)
    sim.run(duration)


Nin = [100, 50, 60, 60, 200, 60]
weight = [0.1*mV, 0.2*mV, 0.3*mV, 0.5*mV, 0.1*mV, 0.5*mV]
fout = [5*Hz, 100*Hz, 10*Hz, 70*Hz, 10*Hz, 400*Hz]

configurations = []
for n, w, f in zip(Nin, weight, fout):
    configurations.append({"Nin": n, "weight": w, "fout": f})

pool = mp.Pool()
results = [pool.apply_async(runsim, kwds=c) for c in configurations]
