# Uncomment the following two lines when running headless
import matplotlib
matplotlib.use('Agg')
from brian import *
import pickle

def clamp(arr, low, high):
    arr=array(arr)
    arr[arr<low] = low
    arr[arr>high] = high
    return arr

# Simulation parameters
defaultclock.dt = dt = 0.1*ms
duration = 0.5*second
nneurons = 3000

# Neuron parameters
cap = 1*uF
gL = 0.1*msiemens
eL = -65*mV
eNa = 55*mV
eK = -90*mV
gNa = 35*msiemens
gK = 9*msiemens
threshold = EmpiricalThreshold(threshold=10*mV, refractory=2*ms)

# Input parameters
taue = 10*ms
taui = 5*ms
eExc = 0*mV
eInh = -80*mV
wExc = 150*nS
wInh = 55*nS

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


print('Network ...')
network = NeuronGroup(nneurons, eqs, threshold=threshold, method='RK')
nExcNrns = int(0.6*nneurons)
nInhNrns = nneurons-nExcNrns
excSubnet = network.subgroup(nExcNrns)
inhSubnet = network.subgroup(nInhNrns)

print('Connections ...')
# External stimuli
inpGrp = PoissonGroup(1000, rates=lambda t: sin(t*10*Hz*2*pi)*20*Hz+20*Hz)
inpConn = Connection(source=inpGrp, target=network,
        state='gExc', delay=(1*ms, 5*ms), sparseness=0.10, weight=wExc)

# Global inhibition
#weights = rand(200, nneurons)*5*uS
#inhGrp = PoissonGroup(200, rates=10*Hz)
#inhConn = Connection(source=inhGrp, target=network, state='gInh',
#        delay=5*ms, sparseness=0.2, weight=wInh)

# Inter-network connections
interExcConn = Connection(excSubnet, network, 'gExc', weight=wExc,
        delay=(1*ms, 5*ms), sparseness=0.01)
interInhConn = Connection(inhSubnet, network, 'gInh', weight=wInh,
        delay=(1*ms, 5*ms), sparseness=0.01)


# Init conditions
network.v = -65*mV
network.h = 1

print('Monitors ...')
# Monitors
inpmon = SpikeMonitor(inpGrp)
spikemon = SpikeMonitor(network)
memmon = StateMonitor(network, 'v', record=True)

print('Running ...')
# Run
run(duration, report='text')

print('%i total spikes fired.' % spikemon.nspikes)

print('Plotting')
# Plotting
inspikes = [isp[1] for isp in inpmon.spikes]
outspikes = [osp[1] for osp in spikemon.spikes]
ion()
subplot(2,2,1)
raster_plot(inpmon)
axis(xmax=duration/ms)
subplot(2,2,2)
hist(inspikes, bins=100)
subplot(2,2,3)
raster_plot(spikemon)
axis(xmax=duration/ms)
subplot(2,2,4)
hist(outspikes, bins=100)
savefig("HHNet.png")

pickle.dump(inpmon.spikes, open("input.pkl", 'w'))
pickle.dump(spikemon.spikes, open("output.pkl", 'w'))
pickle.dump(memmon.values, open("membrane.pkl", 'w'))



