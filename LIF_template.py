from brian import *

duration = 1*second
N_sims = 1

lif_eq = ['dV/dt = (V_rest-V)/tau_mem : volt']
V_rest = 0*mV
V_reset = 0*mV
V_th = 13*mV
t_refr = 2*ms
tau_mem = 10*msecond
N_in = 10
f_in = 50*Hz
DV_s = 2.5*mV

def inputRate(t):
    if t < 500*ms:
        return 50*Hz
    elif 500*ms <= t < 1000*ms:
        return 300*Hz
    else:
        return 50*Hz

inp = PoissonGroup(N_in, rates=inputRate)
nrns = NeuronGroup(N_sims, lif_eq, threshold=V_th, reset=V_reset,\
        refractory=t_refr)
con = Connection(inp, nrns, 'V')
con[:,0] = DV_s
nrns.rest()
mem = StateMonitor(nrns, 'V', record=True)
st = SpikeMonitor(nrns)
inp_mon = SpikeMonitor(inp)
run(duration, report='stdout')

for n in range(N_sims):
    f_out = len(st.spiketimes[n])/duration
    print "Neuron %i firing rate: %s" % (n, f_out)

subplot(2,1,1)
raster_plot(inp_mon)
subplot(2,1,2)
plot(mem.times,mem[0],mem.times,ones(len(mem.times))*V_th)
title('Membrane voltage trace of neuron 0')
xlabel("Time (seconds)")
ylabel("Volts")
show()


