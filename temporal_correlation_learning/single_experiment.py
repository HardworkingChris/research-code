from __future__ import division
from brian import *

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
WExc = 800*nS
WInh = 50*nS

eqs='''
    dV/dt=(-gNa*m**3*h*(V-ENa)-gK*n**4*(V-EK)-gL*(V-EL)-\
                            gExc*(V-EExc)-gInh*(V-EInh)+Iapp)/Cm : volt

    m=alpham/(alpham+betam) : 1

    alpham=-0.1/mV*(V+35*mV)/(exp(-0.1/mV*(V+35*mV))-1)/ms : Hz

    betam=4*exp(-(V+60*mV)/(18*mV))/ms : Hz

    dh/dt=5*(alphah*(1-h)-betah*h) : 1

    alphah=0.07*exp(-(V+58*mV)/(20*mV))/ms : Hz

    betah=1./(exp(-0.1/mV*(V+28*mV))+1)/ms : Hz

    dn/dt=5*(alphan*(1-n)-betan*n) : 1

    alphan=-0.01/mV*(V+34*mV)/(exp(-0.1/mV*(V+34*mV))-1)/ms : Hz

    betan=0.125*exp(-(V+44*mV)/(80*mV))/ms : Hz

    dgExc/dt = -gExc*(1./taue) : siemens

    dgInh/dt = -gInh*(1./taui) : siemens

    Iapp : amp

'''
neuron = NeuronGroup(1, eqs, threshold=threshold, method='RK')

neuron.V = -70*mV

inputs = PoissonGroup(20, rates=20*Hz)
exc_conn = Connection(inputs, neuron, 'gExc', weight=WExc)

vtrace = StateMonitor(neuron, 'V', record=True)
mtrace = StateMonitor(neuron, 'm', record=True)
htrace = StateMonitor(neuron, 'h', record=True)
ntrace = StateMonitor(neuron, 'n', record=True)
exc_trace = StateMonitor(neuron, 'gExc', record=True)

run(1*second)

subplot(311)
plot(vtrace.times, vtrace[0], label="V(t)")
legend()
subplot(312)
plot(mtrace.times, mtrace[0], label="m(t)")
plot(htrace.times, htrace[0], label="h(t)")
plot(ntrace.times, ntrace[0], label="n(t)")
legend()
subplot(313)
plot(exc_trace.times, exc_trace[0], label="gExc")
legend()
show()

