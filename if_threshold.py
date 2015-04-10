from brian import (Network, NeuronGroup, SpikeGeneratorGroup, Connection,
                   StateMonitor, SpikeMonitor,
                   defaultclock,
                   mV, ms, Hz)
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

duration = 2000*ms
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

    fig = plt.figure()
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.set_title("Threshold jump model")
    ax1.plot(thvmon.times, thvmon[0])
    ax1.plot(ththmon.times, ththmon[0], "k--")
    ax1.set_ylabel("membrane potential (V)")

    ax2 = fig.add_subplot(3, 1, 2)
    ax2.set_title("Reset model")
    ax2.plot(resetvmon.times, resetvmon[0], "r")
    ax2.plot(resetthmon.times, resetthmon[0], "k--")
    ax2.set_ylabel("membrane potential (V)")

    ax3 = fig.add_subplot(3, 1, 3)
    ax3.set_title("Spike times and deviations")
    ax3b = ax3.twinx()
    deviations = []
    for spth, sprst in zip(thspikemon[0], resetspikemon[0]):
        ax3.plot([spth]*2, [0, 0.5], "b")
        ax3.plot([sprst]*2, [0.5, 1], "r")
        deviations.append(abs(spth-sprst))
    ax3.axis(xmin=0, xmax=float(duration))

    ax3b.plot(thspikemon[0], deviations, "k--")
    ax3.set_xlabel("time (s)")
    ax3b.set_ylabel("spike time deviation (s)")
    plt.show()
