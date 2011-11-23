#!/usr/bin/env python

from brian import *
from IPython import embed


duration = 10000*ms
lif_eq = ['dV/dt = (-V+V_rest)/tau_mem : volt']
V_rest = 0*mV
V_reset = 0*mV
V_th = 15*mV
t_refr = 2*ms
tau_mem = 10*msecond
N_in = 10
f_in = 10*Hz
V_inp = 0.3*mV
pulse_times = [1*second,2*second,3*second,4*second,5*second,6*second,7*second]
N_in = 200
sigma_in = 300*ms
nrns = NeuronGroup(10,lif_eq,threshold=V_th,reset=V_reset,refractory=t_refr)
input_spikes = []
for st in pulse_times:
    input_spikes.extend(PulsePacket(t=st,n=N_in,sigma=sigma_in).spiketimes)
inp = SpikeGeneratorGroup(N_in, input_spikes)
con = Connection(inp,nrns,'V',weight=V_inp)
mem_mon = StateMonitor(nrns,'V',record=True)
inp_mon = SpikeMonitor(inp)
run(duration,report='stdout')

#subplot(2,1,1)
#raster_plot(inp_mon)
#subplot(2,1,2)
#plot(mem_mon.times,mem_mon[0])
spikes = array([])
for n in inp_mon.getspiketimes():
    spikes = append(spikes, inp_mon.spiketimes[n])
embed() # drop to ipython shell


