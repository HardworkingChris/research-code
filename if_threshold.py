from brian import (Network, NeuronGroup, PoissonGroup, Connection,
                   StateMonitor, SpikeMonitor,
                   mV, ms, Hz)
import matplotlib.pyplot as plt

def pif_th():
    lifeq = """
    V : volt
    Vth : volt
    """
    thstep = 15*mV
    nrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset="Vth+=thstep")
    nrn.V = 0*mV
    nrn.Vth = thstep
    sim = Network(nrn)

    inputgrp = PoissonGroup(20, 20*Hz)
    connection = Connection(inputgrp, nrn, state="V", weight=0.5*mV)

    vmon = StateMonitor(nrn, "V", record=True)
    thmon = StateMonitor(nrn, "Vth", record=True)
    spikemon = SpikeMonitor(nrn, record=True)

    sim.add(inputgrp, connection, vmon, thmon, spikemon)
    sim.run(200*ms)
    return vmon, thmon, spikemon


def pif_reset():
    lifeq = """
    V : volt
    Vth : volt
    """
    thstep = 15*mV
    nrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset="V=0*mV")
    nrn.V = 0*mV
    nrn.Vth = thstep
    sim = Network(nrn)

    inputgrp = PoissonGroup(20, 20*Hz)
    connection = Connection(inputgrp, nrn, state="V", weight=0.5*mV)

    vmon = StateMonitor(nrn, "V", record=True)
    thmon = StateMonitor(nrn, "Vth", record=True)
    spikemon = SpikeMonitor(nrn, record=True)

    sim.add(inputgrp, connection, vmon, thmon, spikemon)
    sim.run(200*ms)
    return vmon, thmon, spikemon


if __name__=="__main__":
    thvmon, ththmon, thspikemon = pif_th()
    print("Finished 1")
    resetvmon, resetthmon, resetspikemon = pif_reset()
    print("Finished 2")


    # plt.figure()
    # plt.plot(vmon.times, vmon[0])
    # plt.plot(thmon.times, thmon[0], "k--")
    # for sp in spikemon[0]:
    #     plt.plot([sp]*2, [0, 0.004], "k")

    # plt.show()
