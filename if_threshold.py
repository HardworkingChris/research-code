from brian import (Network, NeuronGroup, SpikeGeneratorGroup, Connection,
                   StateMonitor, SpikeMonitor,
                   defaultclock,
                   mV, ms, Hz, nA, Mohm)
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
    I = 0.2*nA
    R = 1*Mohm
    lifeq = """
    dV/dt = I*R/ms : volt
    Vth : volt
    """
    thstep = 15*mV
    nrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset="Vth+=thstep")
    nrn.V = 0*mV
    nrn.Vth = thstep
    sim.add(nrn)

    #connection = Connection(inputgrp, nrn, state="V", weight=0.5*mV)
    #sim.add(inputgrp, connection)

    vmon = StateMonitor(nrn, "V", record=True)
    thmon = StateMonitor(nrn, "Vth", record=True)
    spikemon = SpikeMonitor(nrn, record=True)

    sim.add(vmon, thmon, spikemon)
    sim.run(duration)
    return vmon, thmon, spikemon


def pif_reset():
    defaultclock.reinit()
    sim = Network()
    I = 0.2*nA
    R = 1*Mohm
    lifeq = """
    dV/dt = I*R/ms : volt
    Vth : volt
    """
    thstep = 15*mV
    nrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset="V=0*mV")
    nrn.V = 0*mV
    nrn.Vth = thstep
    sim.add(nrn)

    #connection = Connection(inputgrp, nrn, state="V", weight=0.5*mV)
    #sim.add(inputgrp, connection)

    vmon = StateMonitor(nrn, "V", record=True)
    thmon = StateMonitor(nrn, "Vth", record=True)
    spikemon = SpikeMonitor(nrn, record=True)

    sim.add(vmon, thmon, spikemon)
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
    ax1.plot(thvmon.times*1000, thvmon[0]*1000)
    ax1.plot(ththmon.times*1000, ththmon[0]*1000, "k--")
    ax1.set_ylabel("mV")

    ax2 = fig.add_subplot(3, 1, 2)
    ax2.set_title("Reset model")
    ax2.plot(resetvmon.times*1000, resetvmon[0]*1000, "r")
    ax2.plot(resetthmon.times*1000, resetthmon[0]*1000, "k--")
    ax2.set_ylabel("mV")

    ax3 = fig.add_subplot(3, 1, 3)
    ax3.set_title("Spike times and deviations")
    ax3b = ax3.twinx()
    deviations = []
    for spth, sprst in zip(thspikemon[0], resetspikemon[0]):
        ax3.plot([spth*1000]*2, [0, 0.5], "b")
        ax3.plot([sprst*1000]*2, [0.5, 1], "r")
        deviations.append(abs(spth-sprst))
    ax3.axis(xmin=0, xmax=float(duration*1000))

    deviations = np.array(deviations)
    ax3b.plot(thspikemon[0]*1000, deviations*1000, "k--")
    ax3.set_xlabel("time (ms)")
    ax3b.set_ylabel("spike time deviation (ms)")
    plt.show()
