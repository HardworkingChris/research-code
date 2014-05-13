#!/usr/bin/env python

from brian import *



lif_eq = ['dV/dt = (-V+V_rest)/tau_mem : volt']
V_rest = 0*mV
V_reset = 0*mV
V_th = 15*mV
t_refr = 2*ms
tau_mem = 10*msecond
N_in = 10
f_in = 10*Hz
V_inp = 0.3*mV
nrns = NeuronGroup(1,lif_eq,threshold=V_th,reset=V_reset,refractory=t_refr)




