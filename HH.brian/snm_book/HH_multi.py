'''
DELETE: DOESN'T WORK

Hodgkin-Huxley model
Assuming area 1*cm**2

Parameter values as in Spiking Neuron Models book (Gerstner & Kistler)
'''

from brian import *
from brian.library.ionic_currents import *

duration = 1000*ms
N = 100


El = 10.6 * mV
EK = -12 * mV
ENa = 115 * mV
eqs = MembraneEquation(1 * uF) + leak_current(.3 * msiemens, El)
eqs += K_current_HH(36 * msiemens, EK) + Na_current_HH(120 * msiemens, ENa)

neurons = NeuronGroup(N, eqs, threshold=EmpiricalThreshold(threshold=50*mV,refractory=3*ms), implicit=True, freeze=True)


inps = linspace(0*uA,30*uA,N)
freqs = zeros(N)
neurons.I = inps
inp_mon = StateMonitor(neurons, 'I', record=True)
spk_mon = SpikeMonitor(neurons)
run(duration)

for n in spk_mon.spiketimes:
    freqs[n] = len(spk_mon.spiketimes[p])/duration

plot(inps,freqs)


