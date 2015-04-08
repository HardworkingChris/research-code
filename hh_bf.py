from brian import (Network, NeuronGroup, StateMonitor,
                   defaultclock, EmpiricalThreshold, display_in_unit,
                   ms, second, mV, nS, msiemens, uF, uA)
import matplotlib.pyplot as plt
import numpy as np

sim = Network()
defaultclock.dt = dt = 0.1*ms
duration = 0.1*second

# Neuron parameters
Cm = 1*uF # /cm**2
gL = 0.1*msiemens
EL = -65*mV
ENa = 55*mV
EK = -90*mV
gNa = 35*msiemens
gK = 9*msiemens
threshold = EmpiricalThreshold(threshold=15*mV, refractory=2*ms)

# Input parameters
taue = 15*ms
taui = 5*ms
EExc = 0*mV
EInh = -80*mV
WExc = 80*nS
WInh = 50*nS

inputcurrents = [ia*uA for ia in np.arange(0.1, 10.01, 0.01)]

eqs='''
    dv/dt=(-gNa*m**3*h*(v-ENa)-gK*n**4*(v-EK)-gL*(v-EL)-\
                            gExc*(v-EExc)-gInh*(v-EInh)+Iapp)/Cm : volt

    m=alpham/(alpham+betam) : 1

    alpham=-0.1/mV*(v+35*mV)/(exp(-0.1/mV*(v+35*mV))-1)/ms : Hz

    betam=4*exp(-(v+60*mV)/(18*mV))/ms : Hz

    dh/dt=5*(alphah*(1-h)-betah*h) : 1

    alphah=0.07*exp(-(v+58*mV)/(20*mV))/ms : Hz

    betah=1./(exp(-0.1/mV*(v+28*mV))+1)/ms : Hz

    dn/dt=5*(alphan*(1-n)-betan*n) : 1

    alphan=-0.01/mV*(v+34*mV)/(exp(-0.1/mV*(v+34*mV))-1)/ms : Hz

    betan=0.125*exp(-(v+44*mV)/(80*mV))/ms : Hz

    dgExc/dt = -gExc*(1./taue) : siemens

    dgInh/dt = -gInh*(1./taui) : siemens

    Iapp : amp

'''
neuron = NeuronGroup(len(inputcurrents), eqs, threshold=threshold, method='RK')
sim.add(neuron)

# Init conditions
neuron.v = -65*mV
neuron.Iapp = inputcurrents
neuron.h = 1

# Monitors
vmon = StateMonitor(neuron, 'v', record=True)
nmon = StateMonitor(neuron, 'n', record=True)
sim.add(vmon, nmon)

# Run
sim.run(duration, report='text')

plt.figure("Voltage")
plt.plot(vmon.times, vmon[0])

plt.figure("Bifurcation diagram")
for idx, incurrent in enumerate(inputcurrents):
    label = display_in_unit(incurrent, uA)
    plt.clf()
    plt.plot(vmon[idx], nmon[idx], label=label, linestyle="", marker=".")
    plt.axis(xmin=-0.08, xmax=0.08, ymin=0, ymax=1)
    plt.title(label)
    filename = "/home/achilleas/tmp/hh_bf{:04}.png".format(idx)
    plt.savefig(filename)
    print("Saved {}".format(filename))
