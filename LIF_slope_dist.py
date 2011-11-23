#!/usr/bin/env python

from brian import *
import neurotools as nt

LIFeq = ['dv/dt = (-(v-rest))/tc : volt']
tc = 10*ms
rest = 0*mV
thresh = 15*mV

#inp = PoissonGroup(90,100*Hz)
n = 170
s = 0.7
sigma = 0*ms
rate = 50*Hz
dura = 0.5*second
w = 1*mV
dv_spike = 0.1*mV

inp = MultipleSpikeGeneratorGroup(nt.synchinp(n,s,sigma,rate,dura))
lif = NeuronGroup(1,LIFeq,threshold=thresh,reset=0*mV,refractory=2*ms)
con = Connection(inp,lif,'v')
con[:,0] = dv_spike
lif.rest()

mem = StateMonitor(lif, 'v', record=True)
st = SpikeMonitor(lif)
inp_mon = SpikeMonitor(inp)
run(dura)


slopedist = nt.slope_distribution(mem[0],w)
slopedist_pos = nt.positive_slope_distribution(mem[0],w)
pos_slopes = np.diff(mem[0])
pos_slopes = pos_slopes[pos_slopes > 0]


CV = std(st[0])/mean(st[0])
print "CV:",CV
print "Fired",st.nspikes,"spikes"
print "Mean positive slope:",mean(pos_slopes)


subplot(2,2,1)
raster_plot(inp_mon)
title('Inputs')
subplot(2,2,3)
plot(mem.times,mem[0],mem.times,ones(len(mem.times))*thresh)
title('Membrane')
subplot(2,2,2)
bar(slopedist[1][:-1],slopedist[0],float(w))
title('Slope distribution')
subplot(2,2,4)
bar(slopedist_pos[1][:-1],slopedist_pos[0],float(w))
title('Positivle slope distribution')
show()


