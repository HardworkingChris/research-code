"""

Simple (1 spike) STDP example in Brian
======================================

Simple example of a single instance of synaptic plasticity, using the
standard STDP rule in Brian.
A single LIF neuron is stimulated with 6 spikes. The weights and parameters are
calibrated such that the 5th spike triggers a response in the post-synaptic
neuron, in order to show both LTP (on the inputs that fired before the output
spike) and LTD (on the 6th input that fires after the output spike).

"""

from brian import *

eqs = "dV/dt = (Vrest-V)/tau : volt"
Vrest = -65*mV
Vth = -50*mV
tau = 10*ms
trefr = 2*ms

neuron = NeuronGroup(1, eqs, threshold="V>=Vth", refractory=trefr, reset=Vrest)
neuron.V = Vrest

spikes = [(0, 10*ms), (0, 100*ms), (1, 105*ms), (2, 110*ms), (3, 110*ms),
          (4, 112*ms), (5, 115*ms)]
for idx, t in enumerate(linspace(200, 500, 6)):
    t = t*ms
    spikes.append((idx, t))
inputs_group = SpikeGeneratorGroup(6, spikes)
connections = Connection(inputs_group, neuron, state="V")
connections[:,0] = 5.0*mV

tau_pre = 20*ms
tau_post = 20*ms
dA_pre = 0.001
dA_post = -0.001
stdp_eqs = """
dA_pre/dt  = -A_pre/tau_pre   : 1
dA_post/dt = -A_post/tau_post : 1
"""
stdp = STDP(connections, stdp_eqs,
            pre="A_pre+=dA_pre; w+=A_post",
            post="A_post+=dA_post; w+=A_pre",
            wmax=10*mV)

voltmon = StateMonitor(neuron, "V", record=True)
spikemon = SpikeMonitor(neuron)

#pre_mon = StateMonitor(stdp, stdp.pre_group, record=True)

run(0.75*second)

print(connections[:,0])

figure("voltage")
plot(voltmon.times, voltmon[0]*1000)
title("Somatic membrane potential")
xlabel("time (s)")
ylabel("membrane potential (mV)")

figure("weight histogram")
hist(connections.W[:,0]*1000)
title("Histogram of synaptic weights")
xlabel("Weights (mV)")
show()
