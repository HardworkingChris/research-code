# Uncomment the following two lines when running headless
import matplotlib
matplotlib.use('Agg')
from brian import *

defaultclock.dt = dt = 0.1*ms
duration = 1000*ms

# Neuron parameters
cap = 1*uF
gL = 0.1*msiemens
eL = -65*mV
eNa = 55*mV
eK = -90*mV
gNa = 35*msiemens
gK = 9*msiemens
threshold = EmpiricalThreshold(threshold=25*mV, refractory=2*ms)

# Input parameters
taue = 10*ms
taui = 5*ms
eExc = 0*mV
eInh = -80*mV
wExc = 17000*nS
wInh = 100*nS

eqs='''
    dv/dt=(-gNa*m**3*h*(v-eNa)-gK*n**4*(v-eK)-gL*(v-eL)-\
                            gExc*(v-eExc)-gInh*(v-eInh))/cap : volt

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

'''
network = NeuronGroup(2, eqs, threshold=threshold)

# Inputs and connections
inpGrp = SpikeGeneratorGroup(1, [(0, 30*ms)])
inpConn = Connection(source=inpGrp, target=network, state='gExc')
intraConn = Connection(source=network, target=network, state='gExc',
        delay=100*ms, weight=array([[0,wExc],[wExc,0]]))
inpConn[0,0] = wExc

# Init conditions
network.v = -65*mV
network.h = 1

# Monitors
memmon = StateMonitor(network, 'v', record=True)
spikemon = SpikeMonitor(network)
excCondMon = StateMonitor(network, 'gExc', record=True)
inhCondMon = StateMonitor(network, 'gInh', record=True)

# Run
run(duration, report='text')

# Plotting
ax1 = subplot(1,1,1)
ax1.plot(memmon.times, memmon[0], color='black', label='V1')
ax1.plot(memmon.times, memmon[1], color='grey', label='V2')
ax1.scatter(spikemon[0], ones(len(spikemon[0]))*25*mV,
                                            s=80, marker='^', c='black')
ax1.scatter(spikemon[1], ones(len(spikemon[1]))*25*mV,
                                            s=80, marker='^', c='grey')
ax1.legend(loc='upper left')
ax2 = twinx()
ax2.plot(excCondMon.times, excCondMon[0],
        linestyle='--', color='green', label='gExc1')
ax2.plot(excCondMon.times, excCondMon[1],
        linestyle='--', color='red', label='gExc2')
ax2.legend(loc='upper right')
show()
print(spikemon[0])
print('Firing rate: %5.1f Hz' % (spikemon.nspikes/duration))
