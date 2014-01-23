#!/usr/bin/env python

from brian import *
import neurotools as nt

duration = 1*second
N_sims = 3

lif_eq = ['dV/dt = (V_rest-V)/tau_mem : volt']
V_rest = 0*mV
V_reset = 0*mV
V_th = 10*volt # to study "threshold-free" potential
t_refr = 2*ms
tau_mem = 10*ms
N_in = [100, 100, 100]
f_in = [10*Hz, 10*Hz, 10*Hz]
DV_s = [0.3*mV, 0.3*mV, 0.3*mV]
g = [0.0, 0.5, 1] # inhibition parameter 
        # (see second set of reviewer comments of NeCo paper for details)
inp_rates = array([])
for f, v, n in zip(f_in, DV_s, N_in):
    inp_rates = append(inp_rates, ones(n)*f)
inp = PoissonGroup(sum(N_in), inp_rates)
inp_inh = PoissonGroup(sum(N_in), inp_rates)
nrns = NeuronGroup(N_sims, lif_eq, threshold=V_th, reset=V_reset,\
        refractory=t_refr)
con = Connection(inp, nrns, 'V')
con_inh = Connection(inp_inh, nrns, 'V')
cum_N_in = cumsum(N_in)
con[0:cum_N_in[0]-1, 0] = DV_s[0]
con_inh[0:cum_N_in[0]-1, 0] = -g[0]*DV_s[0]
con[cum_N_in[0]:cum_N_in[1]-1, 1] = DV_s[1]
con_inh[cum_N_in[0]:cum_N_in[1]-1, 1] = -g[1]*DV_s[1]
con[cum_N_in[1]:cum_N_in[2]-1, 2] = DV_s[2]
con_inh[cum_N_in[1]:cum_N_in[2]-1, 2] = -g[2]*DV_s[2]

nrns.rest()

mem = StateMonitor(nrns, 'V', record=True)
st = SpikeMonitor(nrns)
inp_mon = SpikeMonitor(inp)
print "Running %d simulations ... " % N_sims
run(duration, report='stdout')

for n in range(N_sims):
    mean_est = tau_mem*N_in[n]*f_in[n]*DV_s[n]*(1-g[n])
    var_est = tau_mem*f_in[n]*N_in[n]*(DV_s[n]**2)*(1+g[n]**2)/2

    mean_true = mean(mem[n])*volt
    var_true = var(mem[n])*volt**2
    
    abs_mean_error = abs(mean_est-mean_true)
    abs_var_error = abs(var_est-var_true)
    
    rel_mean_error = abs_mean_error/(mean_true+mean_est)
    rel_var_error = abs_var_error/(var_true+var_est)
    print "Mean membrane potential: % 30s\t-\t% 30s \t=\t% 30s (%s)" %\
        (mean_est, mean_true, abs_mean_error, rel_mean_error)
    print "Variance               : % 30s\t-\t% 30s \t=\t% 30s (%s)" %\
        (var_est, var_true, abs_var_error, rel_var_error)
    hold(True)
    plot(mem.times, mem[n], label='g: %f' % g[n])
legend()
show()

