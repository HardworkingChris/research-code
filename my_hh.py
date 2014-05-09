#import matplotlib
#matplotlib.use('Agg')
from brian import *
from brian.library.ionic_currents import *

defaultclock.dt = dt = 0.1*ms
duration = 0.5*second

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
neuron = NeuronGroup(2, eqs, threshold=threshold, method='RK')


# Inputs and connections
PExc_spikes = PoissonGroup(N=500, rates=8*Hz)
conn = Connection(PExc_spikes, neuron[0], 'gExc', weight=WExc)
PInh = PoissonInput(target=neuron[0], N=1000, rate=5*Hz,
        weight=WInh, state='gInh')

#nsync = 200
#times = cumsum(rand(50))
#times = times/max(times)*(duration*0.95)
#input_times = [(i, t) for i in range(nsync) for t in times]
#inputs = SpikeGeneratorGroup(nsync, input_times)
#inpConn = Connection(inputs, neuron[1], state='gExc', weight=WExc)

pinput = PoissonInput(neuron[1], N=1, rate=10*Hz, weight=WExc, state='gExc',
        copies=200, jitter=0.001)

# Init conditions
neuron.v = -65*mV
neuron.h = 1

# Monitors
inpmon = SpikeMonitor(PExc_spikes)
memmon = StateMonitor(neuron, 'v', record=True)
spikemon = SpikeMonitor(neuron)
excCondMon = StateMonitor(neuron, 'gExc', record=True)
inhCondMon = StateMonitor(neuron, 'gInh', record=True)
iappmon = StateMonitor(neuron, 'Iapp', record=True)

# Run
run(duration, report='text')

# Plotting
subplot(2,1,1)
raster_plot(inpmon)
title('Input spikes')
subplot(2,1,2)
plot(memmon.times/ms, memmon[0]/mV, color='black', label='V(t)')
title('Membrane')
xlabel("Time (ms)")
ylabel("Membrane potential (mV)")
#ax1.scatter(spikemon[0], ones(len(spikemon[0]))*25*mV, s=40, marker='*')
#ax1.legend(loc='upper left')
#ax2 = twinx()
#ax2.plot(excCondMon.times, excCondMon[0],
#        linestyle='--', color='green', label='gExc')
#ax2.plot(inhCondMon.times, -1*inhCondMon[0],
#        linestyle='--', color='red', label='gInh')
#ax2.legend(loc='upper right')
#print(spikemon[0])
#print('Firing rate: %f Hz' % (spikemon.nspikes/duration))
show()

#plot(memmon.times, memmon[0])
#plot(memmon.times, memmon[1])
#savefig('figure.png')

