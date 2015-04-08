from brian import (Network, NeuronGroup, StateMonitor, SpikeMonitor,
                   Connection,
                   mV, ms, Hz)
import matplotlib.pyplot as plt
import spikerlib as sl
import numpy as np
import sys

sim = Network()
duration = 200*ms
dt = 0.1*ms
tau = 10*ms
Vth = 15*mV
Vreset = 0*mV
Vreset = 13.65*mV
lifeq = "dV/dt = -V/tau : volt"

lifnrn = NeuronGroup(1, lifeq, threshold="V>=Vth", reset=Vreset)
lifnrn.V = Vreset
sim.add(lifnrn)

Nin = 200
fin = 40*Hz
Sin = 0.6
sigma = 0.0*ms
weight = 0.1*mV
inputs = sl.tools.fast_synchronous_input_gen(Nin, fin, Sin, sigma, duration)
connection = Connection(inputs, lifnrn, "V", weight=weight)
sim.add(inputs, connection)

vmon = StateMonitor(lifnrn, "V", record=True)
spikemon = SpikeMonitor(lifnrn)
sim.add(vmon, spikemon)

sim.run(duration)
if spikemon.nspikes == 0:
    print("No spikes fired")
    sys.exit(1)

vmon.insert_spikes(spikemon, 40*mV)

high, low = sl.tools.get_slope_bounds(spikemon[0], 0*mV, Vreset, Vth, tau, dt)

plt.figure()
plt.plot(vmon.times*1000, vmon[0]*1000)
plt.plot(vmon.times*1000, np.zeros_like(vmon[0])+Vth*1000, "k--")
plt.plot(np.arange(0*dt, len(high)*dt, dt)*1000, high*1000, color="0.25")
plt.plot(np.arange(0*dt, len(low)*dt, dt)*1000,  low*1000,  color="0.25")

for sp in spikemon[0]:
    plt.plot([(sp-0.002)*1000]*2, [0*mV, Vth*1000], 'r-')

plt.xlabel("t (ms)")
plt.ylabel("Membrane potential (mV)")

plt.show()
