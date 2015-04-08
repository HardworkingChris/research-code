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
high *= 1000
low *= 1000
Vth = float(Vth*1000)

plt.figure()
plt.plot(vmon.times*1000, vmon[0]*1000, label="$V(t)$")
plt.plot(vmon.times*1000, np.zeros_like(vmon[0])+Vth, "k--", label="$V_{th}$")
plt.plot(np.arange(0*dt, len(high)*dt, dt)*1000, high, color="0.25",
         label="bounds")
plt.plot(np.arange(0*dt, len(low)*dt, dt)*1000,  low,  color="0.25")
#plt.legend()

for idx, sp in enumerate(spikemon[0], 1):
    sp *= 1000
    ws = sp-2
    vws = vmon[0][ws*10]*1000
    plt.plot([(ws)]*2, [0, Vth], 'r-')
    plt.plot(ws, vws, 'k.', markersize=10)
    plt.plot(sp, Vth, 'k.', markersize=10)
    plt.annotate("$V(t_{}-w)$".format(idx), xy=(ws, vws),
                 xytext=(ws+0.1, vws-1), backgroundcolor=(1,1,1,0.5))
    plt.annotate("$V(t_{})$".format(idx), xy=(sp, Vth),
                 xytext=(sp+0.1, Vth+0.1), backgroundcolor=(1,1,1,0.5))

plt.xlabel("t (ms)")
plt.ylabel("Membrane potential (mV)")

plt.show()
