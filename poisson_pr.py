#!/usr/bin/env python

from brian import *

#--------- Neuron parameters -----------#
tc = 10*ms
Vrest = 0*mV
Vth = 15*mV
beta = 0.91
Vreset = (Vth - Vrest)*beta + Vrest
refr = 0*ms
#--------- Neuron equation -------------#
LIFeq = ['dv/dt = (-(v-Vrest))/tc : volt']



allCV = []
allmISI = []

#--------- Neuron input ----------------#
inrates = range(170,250,1)
#---------------------------------------#


lif = NeuronGroup(len(inrates),LIFeq,threshold=Vth,reset=Vreset,refractory=refr)

con = []
for i in range(0,len(inrates)):
    con.append(Connection(PoissonGroup(50,inrates[i]*Hz),lif[i],'v'))
    con[i][:,0] = 0.16*mV

lif.rest()
spiketimes = SpikeMonitor(lif)
mem = StateMonitor(lif,'v',record=True)

print "Running",len(lif),"neurons"
run(10*second)
print "Done!"

for i in range(0,len(inrates)):
    isi = diff(spiketimes[i])
    misi = mean(isi)*second
    CV = std(isi)*second/misi
    allCV.append(CV)
    allmISI.append(misi)
#    print "Plotting",i
#    figure()
#    plot(mem[i])
#    xlabel("input rate: {rate}".format(rate=inrates[i]))
#    title("CV: {0}, ISI: {1} ({2})".format(CV,misi,1/misi))

plot(allmISI,allCV,'o')
show()
#subplot(311)
#raster_plot(inp)
#subplot(312)
#plot(mem.times,mem[0],mem.times,ones(len(mem.times))*Vth)
#subplot(313)
#raster_plot(st)
#show()


