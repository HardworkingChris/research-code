from __future__ import print_function, division
from brian import (Network, NeuronGroup, SpikeMonitor,
                   PoissonGroup, Connection,
                   mV, ms, Hz)
import sys
import matplotlib.pyplot as plt
import numpy as np
import itertools as itt

fin = [f*Hz for f in range(10, 41, 5)]
win = [w*mV for w in np.arange(0.5, 2.1, 0.5)]
Nin = [n for n in range(100, 181, 20)]
tau = 10*ms
Vth = 15*mV
reset = 0*mV

configs = [c for c in itt.product(Nin, fin, win)]
Nsims = len(configs)
print("Number of configurations: {}".format(Nsims))

lifeq = "dV/dt = -V/tau : volt"
sim = Network()
nrn = NeuronGroup(Nsims, lifeq, threshold="V>=Vth", reset="V=reset")
inputgroups = []
connections = []
print("Setting up ...")
for idx, c in enumerate(configs):
    n, f, w = c
    inp = PoissonGroup(n, f)
    conn = Connection(inp, nrn[idx], state="V", weight=w)
    inputgroups.append(inp)
    connections.append(conn)
    print("\r{}/{}".format(idx+1, Nsims), end="")
    sys.stdout.flush()
print()

spikemon = SpikeMonitor(nrn)

sim.add(*inputgroups)
sim.add(*connections)
sim.add(nrn)
sim.add(spikemon)

duration = 1000*ms
print("Running for {} s".format(duration))
sim.run(duration, report="text")

plt.figure()
inputvolts = np.array([c[0]*c[1]*c[2]*tau for c in configs])
spikerates = np.array([len(sp) for sp in spikemon.spiketimes.itervalues()])
for idx in range(Nsims):
    iv = inputvolts[idx]
    sr = spikerates[idx]
    plt.plot(iv, sr, "b.")
    print("{} mV -> {} Hz".format(iv*1000, sr/duration))
ivsorted = np.sort(inputvolts)
theofout = 1.0/(tau*np.log(ivsorted/(ivsorted-Vth)))
theovin = Vth/(1-np.exp(-1.0/(tau*spikerates)))
plt.plot(ivsorted, theofout, "r-")
sidx = np.argsort(theovin)
plt.plot(theovin[sidx], spikerates[sidx], "g-")

Narr = np.array([c[0] for c in configs])
Warr = np.array([c[1] for c in configs])
farr = np.array([c[2] for c in configs])
theofin = Vth/((1-np.exp(-1.0/(tau*spikerates)))*Narr*Warr*tau)
plt.figure()
plt.plot(theofin, farr, "b.")
plt.plot([min(theofin), max(theofin)], [min(theofin), max(theofin)], 'k--')

plt.show()
