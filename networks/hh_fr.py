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
WExc = 2*nS
WInh = 1*nS

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
RatesExc = frange(0, 500, 50)
RatesInh = [0, 30, 100]

Nneurons = len(RatesExc)*len(RatesInh)
neurons = NeuronGroup(Nneurons, eqs, threshold=threshold)

# Inputs and connections
i=0
ExcInps = []
InhInps = []
configs = []
for exc in RatesExc:
    for inh in RatesInh:
        ExcInps.append(PoissonInput(target=neurons[i], N=10000, weight=WExc,
            rate=exc, state='gExc'))
        InhInps.append(PoissonInput(target=neurons[i], N=2000, weight=WInh,
            rate=inh, state='gInh'))
        configs.append((exc, inh))
        i+=1

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
frates = [len(s)/duration for s in spikemon.spiketimes.values()]
frates = reshape(frates, (len(RatesExc), len(RatesInh)))
plot(RatesExc, frates)
legend(RatesInh, loc='best')
xlabel('Exc. input rate')
ylabel('Firing rate')
ion()
show()

