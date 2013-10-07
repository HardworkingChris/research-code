# Uncomment the following two lines when running headless
#import matplotlib
#matplotlib.use('Agg')
from brian import *

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
network_sync = NeuronGroup(nneurons, eqs, threshold=threshold, method='RK')
nExcNrns = int(0.6*nneurons)
nInhNrns = nneurons-nExcNrns
excSubnet_sync = network_sync.subgroup(nExcNrns)
inhSubnet_sync = network_sync.subgroup(nInhNrns)

network_rand = NeuronGroup(nneurons, eqs, threshold=threshold, method='RK')
excSubnet_rand = network_rand.subgroup(nExcNrns)
inhSubnet_rand = network_rand.subgroup(nInhNrns)


print('Connections ...')
# External stimuli
inpGrp_sync = PoissonGroup(1000,
        rates=lambda t: sin(t*10*Hz*2*pi)*20*Hz+20*Hz)
inpConn_sync = Connection(source=inpGrp_sync, target=network_sync,
        state='gExc', delay=(1*ms, 5*ms), sparseness=0.10, weight=wExc)

inpGrp_rand = PoissonGroup(1000, rates=20*Hz)
inpConn_rand = Connection(source=inpGrp_rand, target=network_rand,
        state='gExc', delay=(1*ms, 5*ms), sparseness=0.10, weight=wExc)

# Global inhibition
#weights = rand(200, nneurons)*5*uS
#inhGrp = PoissonGroup(200, rates=10*Hz)
#inhConn = Connection(source=inhGrp, target=network, state='gInh',
#        delay=5*ms, sparseness=0.2, weight=wInh)

# Inter-network connections
interExcConn_sync = Connection(excSubnet_sync, network_sync, 'gExc',
        weight=wExc, delay=(1*ms, 5*ms), sparseness=0.01)
interInhConn_sync = Connection(inhSubnet_sync, network_sync, 'gInh',
        weight=wInh, delay=(1*ms, 5*ms), sparseness=0.01)

interExcConn_rand = Connection(excSubnet_rand, network_rand, 'gExc',
        weight=wExc, delay=(1*ms, 5*ms), sparseness=0.01)
interInhConn_rand = Connection(inhSubnet_rand, network_rand, 'gInh',
        weight=wInh, delay=(1*ms, 5*ms), sparseness=0.01)

# Init conditions
network_sync.v = -65*mV
network_sync.h = 1

network_rand.v = -65*mV
network_rand.h = 1

print('Monitors ...')
# Monitors
inpmon_sync = SpikeMonitor(inpGrp_sync)
spikemon_sync = SpikeMonitor(network_sync)
memmon_sync = StateMonitor(network_sync, 'v', record=True)

inpmon_rand = SpikeMonitor(inpGrp_rand)
spikemon_rand = SpikeMonitor(network_rand)
memmon_rand = StateMonitor(network_rand, 'v', record=True)


print('Running ...')
# Run
run(duration, report='text')


print('Plotting')
# Plotting
inspikes_sync = [isp[1] for isp in inpmon_sync.spikes]
outspikes_sync = [osp[1] for osp in spikemon_sync.spikes]
inspikes_rand = [isp[1] for isp in inpmon_rand.spikes]
outspikes_rand = [osp[1] for osp in spikemon_rand.spikes]
ion()
subplot(2,2,1)
raster_plot(inpmon_sync)
axis(xmax=duration/ms)
subplot(2,2,2)
hist(inspikes_sync, bins=100)
subplot(2,2,3)
raster_plot(spikemon_sync)
axis(xmax=duration/ms)
subplot(2,2,4)
hist(outspikes_sync, bins=100)

figure()
subplot(2,2,1)
raster_plot(inpmon_rand)
axis(xmax=duration/ms)
subplot(2,2,2)
hist(inspikes_rand, bins=100)
subplot(2,2,3)
raster_plot(spikemon_rand)
axis(xmax=duration/ms)
subplot(2,2,4)
hist(outspikes_rand, bins=100)


