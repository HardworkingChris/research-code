from brian import (Network, NeuronGroup, SpikeGeneratorGroup, Connection,
                   StateMonitor, SpikeMonitor,
                   defaultclock,
                   mV, ms, Hz)
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

duration = 200*ms
inspikes = []
while np.sum(inspikes) < float(duration):
    inspikes.append(rnd.expovariate(500*Hz))
inspikes = np.cumsum(inspikes)
spiketuples = [(0, t) for t in inspikes]
inputgrp = SpikeGeneratorGroup(1, spiketuples)


def pif_th():
    defaultclock.reinit()
    sim = Network()
    lifeq = """
    V : volt
    Vth : volt
    """
    thstep = 15*mV
    nrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset="Vth+=thstep")
    nrn.V = 0*mV
    nrn.Vth = thstep
    sim.add(nrn)

    connection = Connection(inputgrp, nrn, state="V", weight=0.5*mV)

    vmon = StateMonitor(nrn, "V", record=True)
    thmon = StateMonitor(nrn, "Vth", record=True)
    spikemon = SpikeMonitor(nrn, record=True)

    sim.add(inputgrp, connection, vmon, thmon, spikemon)
    sim.run(duration)
    return vmon, thmon, spikemon


def pif_reset():
    defaultclock.reinit()
    sim = Network()
    lifeq = """
    V : volt
    Vth : volt
    """
    thstep = 15*mV
    nrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset="V=0*mV")
    nrn.V = 0*mV
    nrn.Vth = thstep
    sim.add(nrn)

    connection = Connection(inputgrp, nrn, state="V", weight=0.5*mV)

    vmon = StateMonitor(nrn, "V", record=True)
    thmon = StateMonitor(nrn, "Vth", record=True)
    spikemon = SpikeMonitor(nrn, record=True)

    sim.add(inputgrp, connection, vmon, thmon, spikemon)
    sim.run(duration)
    return vmon, thmon, spikemon


if __name__=="__main__":
    thvmon, ththmon, thspikemon = pif_th()
    print("Finished 1")
    resetvmon, resetthmon, resetspikemon = pif_reset()
    print("Finished 2")

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(thvmon.times, thvmon[0])
    plt.plot(ththmon.times, ththmon[0], "k--")
    plt.subplot(3, 1, 2)
    plt.plot(resetvmon.times, resetvmon[0], "r")
    plt.plot(resetthmon.times, resetthmon[0], "k--")
    plt.subplot(3, 1, 3)
    for sp in thspikemon[0]:
        plt.plot([sp]*2, [0, 0.5], "b")
    for sp in resetspikemon[0]:
        plt.plot([sp]*2, [0.5, 1], "r")
    plt.axis(xmin=0, xmax=float(duration))

    plt.show()
