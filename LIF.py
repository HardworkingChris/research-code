#!/usr/bin/env python

from brian import *

duration = 1*second
N_sims = 1

lif_eq = ['dV/dt = (V_rest-V)/tau_mem : volt']
V_rest = 0*mV
V_reset = 13*mV
V_th = 15*mV
t_refr = 2*ms
tau_mem = 10*msecond
N_in = 100
f_in = 20*Hz
DV_s = 1*mV
inp = PoissonGroup(N_in,f_in)
nrns = NeuronGroup(N_sims,lif_eq,threshold=V_th,reset=V_reset,\
        refractory=t_refr)
con = Connection(inp,nrns,'V')
con[:,0] = DV_s
nrns.rest()

mem = StateMonitor(nrns, 'V', record=True)
st = SpikeMonitor(nrns)
inp_mon = SpikeMonitor(inp)
run(duration)

mem.insert_spikes(st, 17*mV)

print "Neuron(s) fired at: ",st.spiketimes
print "Input rate voltage:\t\t",N_in*f_in*DV_s*tau_mem
print "Mean membrane potential:\t",mean(mem[0])*volt


plot(mem.times,mem[0],mem.times,ones(len(mem.times))*V_th)
title('Membrane')
show()


