from brian import *
from brian.library.ionic_currents import *

defaultclock.dt = dt = 0.1*ms
duration = 1000*ms

# Neuron parameters
Cm = 1*uF # /cm**2
gL = 0.1*msiemens
EL = -65*mV
ENa = 55*mV
EK = -90*mV
gNa = 35*msiemens
gK = 9*msiemens
threshold = EmpiricalThreshold(threshold=25*mV, refractory=2*ms)

# Input parameters
taue = 10*ms
taui = 5*ms
EExc = 0*mV
EInh = -80*mV
WExc = 200*nS
WInh = 50*nS

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


neurons = NeuronGroup(2, eqs, threshold=threshold)
nInputs = 1000
S = 0.8

# Inputs and connections
CommonExc = PoissonInput(target=neurons, N=nInputs*(1-S), rate=5*Hz,
            weight=WExc, state='gExc', record=True)
RandExc = PoissonInput(target=neurons[0], N=nInputs*S, rate=5*Hz, weight=WExc,
            state='gExc', record=True)
CommonInh = PoissonInput(target=neurons, N=nInputs, rate=15*Hz,
            weight=WInh, state='gInh', record=True)
SyncExc = PoissonInput(target=neurons[1], N=1, rate=5*Hz,
            weight=WExc*nInputs*S, state='gExc', copies=nInputs*S, record=True)

# Init conditions
neurons.v = -65*mV
neurons.h = 1

# Monitors
memmon = StateMonitor(neurons, 'v', record=True)
spikemon = SpikeMonitor(neurons)
excmon = StateMonitor(neurons, 'gExc', record=True)
inhmon = StateMonitor(neurons, 'gInh', record=True)

# Run
run(duration, report='text')

# Plotting
plot(memmon.times, memmon[0], 'b-', label='S=0.0')
plot(memmon.times, memmon[1], 'r-', label='S=0.8')
legend()

