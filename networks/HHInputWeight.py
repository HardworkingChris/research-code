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
WExc = frange(1000, 2000, 5)*nS
WInh = frange(100, 200, 5)*nS
WInh = zeros(10)*nS
Nneurons = len(WExc)*len(WInh)

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
neurons = NeuronGroup(Nneurons, eqs, threshold=threshold)

# Inputs and connections
PExc = PoissonGroup(N=1000, rates=100*Hz)
PInh = PoissonGroup(N=1000, rates=10*Hz)

CMExc = ones([1000, len()])*WExc
CMInh = ones([1000, len()])*WInh

CExc = Connection(source=PExc, target=neurons, state='gExc', weight=CMExc)
CInh = Connection(source=PInh, target=neurons, state='gInh', weight=CMInh)

# Init conditions
neurons.v = -65*mV
neurons.h = 1

# Monitors
memmon = StateMonitor(neurons, 'v', record=True)
spikemon = SpikeMonitor(neurons)
#ExcCondMon = StateMonitor(neurons, 'gExc', record=True)
#InhCondMon = StateMonitor(neurons, 'gInh', record=True)

# Run
run(duration, report='text')

# Plotting
rates = [len(s) for s in spikemon.spiketimes.values()]
rates = reshape(rates, [len(WInh), len(WExc)])
imshow(rates, aspect='auto', origin='lower', interpolation='none')
        #extent=(min(WExc), max(WExc), min(WInh), max(WInh)))
show()

