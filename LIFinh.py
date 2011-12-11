#!/usr/bin/env python

from brian import *

duration = 1*second
N_sims = 1

lif_eq = ['dV/dt = (V_rest-V)/tau_mem : volt']
V_rest = 0*mV
V_reset = 0*mV
V_th = 15*mV
t_refr = 2*ms
tau_mem = 10*msecond
N_in = 2000
f_in = 5*Hz
involt_exc = 0.35*mV
involt_inh = -0.2*mV
inp = PoissonGroup(N_in, f_in)
nrns = NeuronGroup(N_sims, lif_eq, threshold=V_th, reset=V_reset,\
        refractory=t_refr)
con = Connection(inp, nrns, 'V')
N_exc = int(floor(N_in/2))
N_inh = N_in - N_exc
con[0:N_exc-1,0] = involt_exc
con[N_exc:N_in,0] = involt_inh
nrns.rest()
# monitors #
inp_exc_mon = SpikeMonitor(inp.subgroup(N_exc))
inp_inh_mon = SpikeMonitor(inp.subgroup(N_inh))
mem = StateMonitor(nrns, 'V', record=True)
st = SpikeMonitor(nrns)
###########
run(duration, report='stdout')

for n in range(N_sims):
    f_out = len(st.spiketimes[n])/duration
    print "Neuron %i firing rate: %s" % (n, f_out)

subplot(2,1,1)
raster_plot(inp_exc_mon, inp_inh_mon, showgrouplines=True,\
        spacebetweengroups=0.1)
subplot(2,1,2)
plot(mem.times,mem[0],mem.times,ones(len(mem.times))*V_th)
title('Membrane voltage trace of neuron 0')
xlabel("Time (seconds)")
ylabel("Volts")
show()


