from brian import (Network, NeuronGroup, StateMonitor, SpikeMonitor,
                   Connection,
                   mV, ms, Hz)
import matplotlib.pyplot as plt
import spikerlib as sl
import numpy as np

sim = Network()
duration = 200*ms
tau = 10*ms
Vth = 15*mV
Vreset = 0*mV
lifeq = "dV/dt = -V/tau : volt"

lifnrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset=Vreset)
lifnrn.V = Vreset
sim.add(lifnrn)

Nin = 300
fin = 40*Hz
Sin = 0.6
sigma = 0.5*ms
weight = 0.1*mV
inputs = sl.tools.fast_synchronous_input_gen(Nin, fin, Sin, sigma, duration)
connection = Connection(inputs, lifnrn, "V", weight=weight)
sim.add(inputs, connection)

vmon = StateMonitor(lifnrn, "V", record=True)
spikemon = SpikeMonitor(lifnrn)
sim.add(vmon, spikemon)

sim.run(duration)
vmon.insert_spikes(spikemon, 40*mV)

plt.figure()
plt.plot(vmon.times*1000, vmon[0]*1000)
plt.plot(vmon.times*1000, np.zeros_like(vmon[0])+Vth*1000, "k--")
plt.xlabel("t (ms)")
plt.ylabel("Membrane potential (mV)")
plt.show()
