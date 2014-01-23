from brian import *

duration = 1*second
N_sims = 1

lif_eq = ['dV/dt = (V_rest-V)/tau_mem : volt']
V_rest = -70*mV
V_reset = -60*mV
V_th = -50*mV
t_refr = 2*ms
tau_mem = 10*msecond
N_in = 1
f_in = 50*Hz
DV_s = 2.5*mV
excinp = PoissonGroup(N_in, f_in)
inhinp = PoissonGroup(N_in, f_in)
nrns = NeuronGroup(N_sims, lif_eq, threshold=V_th, reset=V_reset,\
        refractory=t_refr)
exccon = Connection(excinp, nrns, 'V')
inhcon = Connection(inhinp, nrns, 'V')
exccon[:,0] = DV_s
inhcon[:,0] = -DV_s
nrns.rest()
mem = StateMonitor(nrns, 'V', record=True)
st = SpikeMonitor(nrns)
excinp_mon = SpikeMonitor(excinp)
inhinp_mon = SpikeMonitor(inhinp)
run(duration, report='stdout')

for n in range(N_sims):
    f_out = len(st.spiketimes[n])/duration
    print "Neuron %i firing rate: %s" % (n, f_out)

#subplot(2,1,1)
#raster_plot(inp_mon)
#subplot(2,1,2)
#plot(mem.times,mem[0],mem.times,ones(len(mem.times))*V_th)
#title('Membrane voltage trace of neuron 0')
#xlabel("Time (seconds)")
#ylabel("Volts")
#show()


