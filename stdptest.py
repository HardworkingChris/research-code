#!/usr/bin/env python
#import brian_no_units

from brian import *

# We'll use a standard _normalised_ LIF
# V_rest = 0 implicitly



# Parameters

duration = 100*second

# Neuron parameters
N_neurons = 100                 
N_inputs = 10                  
N_outputs = 10                
rate_extinp = 1*Hz           
V_th = 1*mV                 
tau_m = 10*ms              
V_reset = 0*mV            
t_refr = 1*ms            

# Connection parameters
P_conn_ext = 0.1        
P_conn_int = 1.0       
P_conn_out = 0.1
weight_init_ext = 1.0*mV #rand(N_inputs, N_neurons) * 0.1*mV 
weight_init_int = rand(N_neurons, N_neurons) * 0.1*mV 
weight_init_out = rand(N_neurons, N_outputs) * 0.1*mV
weight_max = 0.5*mV

# STDP parameters
tau_pre = 20*ms
tau_post = 20*ms
dA_pre = 0.01
dA_post = -dA_pre * tau_pre / tau_post * 1.05


# LIF equation (no resting potential)
neuron_eqs = '''dV/dt = -V/tau_m : volt'''
nnet = NeuronGroup(N_neurons,neuron_eqs,threshold='V>V_th',reset=V_reset,refractory=t_refr)
# defining output neurons separately
outnet = NeuronGroup(N_outputs, neuron_eqs, threshold='V>V_th', reset=V_reset, refractory=t_refr)


# external Poisson inputs
inp = PoissonGroup(N_inputs,rates=rate_extinp)

# synaptic connections
ext_conn = Connection(inp, nnet, 'V', delay=True, weight=weight_init_ext, structure='sparse', sparseness=P_conn_ext)
int_conn = Connection(nnet, nnet, 'V', delay=True, weight=weight_init_int, structure='dense')
out_conn = Connection(nnet, outnet, 'V', delay=True, weight=weight_init_out, structure='sparse', sparseness=P_conn_out)

# STDP equation 
# copied from http://www.briansimulator.org/docs/examples-plasticity_STDP1.html
eqs_stdp = '''
dA_pre/dt=-A_pre/tau_pre : 1
dA_post/dt=-A_post/tau_post : 1
'''
dA_post *= weight_max
dA_pre *= weight_max
#stdp_ext = STDP(ext_conn, eqs=eqs_stdp, pre='A_pre+=dA_pre;w+=A_post', post='A_post+=dA_post;w+=A_pre', wmin=-weight_max, wmax=weight_max)
stdp_int = STDP(int_conn, eqs=eqs_stdp, pre='A_pre+=dA_pre;w+=A_post', post='A_post+=dA_post;w+=A_pre', wmin=-weight_max, wmax=weight_max)
stdp_out = STDP(out_conn, eqs=eqs_stdp, pre='A_pre+=dA_pre;w+=A_post', post='A_post+=dA_post;w+=A_pre', wmin=-weight_max, wmax=weight_max)


# Monitors
inp_spikes = SpikeMonitor(inp)
int_spikes = SpikeMonitor(nnet)
out_spikes = SpikeMonitor(outnet)



run(10*second, report='text',report_period=5*second)

print "Average input rate:",(float(inp_spikes.nspikes)/N_inputs)/duration
print "Average internal rate:",(float(int_spikes.nspikes)/N_neurons)/duration
print "Average output rate:",(float(out_spikes.nspikes)/N_outputs)/duration

subplot(311)
raster_plot(inp_spikes)
subplot(312)
raster_plot(int_spikes)
subplot(313)
raster_plot(out_spikes)
show()


