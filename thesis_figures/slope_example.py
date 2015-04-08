from brian import (Network, NeuronGroup, StateMonitor, SpikeMonitor,
                   Connection,
                   mV, ms, Hz)
import matplotlib.pyplot as plt
import spikerlib as sl

sim = Network()
duration = 200*ms
tau = 10*ms
Vth = 15*mV
Vreset = 0*mV
lifeq = "dV/dt = -V/tau : volt"

lifnrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset=Vreset)
lifnrn.V = Vreset
sim.add(lifnrn)

Nin = 200
fin = 20*Hz
Sin = 0.3
sigma = 1*ms
weight = 0.2*mV
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
plt.xlabel("t (ms)")
plt.ylabel("Membrane potential (mV)")
plt.show()
