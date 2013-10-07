# Fully connected feed-foward network of identical neurons. Each layer
# has the same amount of neurons connected with synapses with random
# weight. With the appropriate parameter configuration the network can
# keep a stable propagation going indefinitely after initial
# stimulation.


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
duration = 2*second
nneurons = 1000
nlayers = 10

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
wExc = 200*nS
wInh = 30*nS

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


print('Network')
network = NeuronGroup(nneurons, eqs, threshold=threshold)

print('Connections')
# Inter-layer connections
nperlayer = int(nneurons/nlayers)
endpoints = frange(0, nneurons, nperlayer)
if endpoints[-1] > nneurons:
    endpoints = endpoints[:-1]
    print('Network separation into layers has %i leftovers.' % (
        nneurons-endpoints[-1]-1))
layerConns = []
for pre, post in zip(endpoints[:-2], endpoints[1:-1]):
    preG = network[pre:pre+nperlayer]
    postG = network[post:post+nperlayer]
    weights=rand(nperlayer,nperlayer)*1*uS
    newcons = Connection(source=preG, target=postG, state='gExc',
            delay=10*ms, weight=copy(weights))
    layerConns.append(newcons)
# last to first
preG = network[endpoints[-2]:endpoints[-1]]
postG = network[endpoints[0]:endpoints[1]]
weights = rand(nperlayer,nperlayer)*1*uS
newcons = Connection(source=preG, target=postG, state='gExc',
        delay=10*ms, weight=copy(weights))
layerConns.append(newcons)

# External stimuli
def initRates(t):
    if t < 60*ms:
        return 100*Hz
    else:
        return 0*Hz
weights = rand(20, nperlayer)*0.5*uS
inpGrp = PoissonGroup(20, rates=initRates)
inpConn = Connection(source=inpGrp, target=network[:nperlayer], state='gExc',
        delay=5*ms, weight=copy(weights))

# Global inhibition
#weights = rand(20, nneurons)*30*uS
#inhGrp = PoissonGroup(20, rates=40*Hz)
#inhConn = Connection(source=inhGrp, target=network, state='gInh',
#        delay=5*ms, weight=copy(weights))
#

# Init conditions
network.v = -65*mV
network.h = 1

print('Monitors')
# Monitors
inpmon = SpikeMonitor(inpGrp)
spikemon = SpikeMonitor(network)
memmon = StateMonitor(network, 'v', record=True)
#hmon = StateMonitor(network, 'h', record=0)

print('Running')
# Run
run(duration, report='text')

print('%i total spikes fired.' % spikemon.nspikes)

print('Plotting')
# Plotting
subplot(2,1,1)
raster_plot(inpmon)
axis(xmax=duration/ms)
subplot(2,1,2)
raster_plot(spikemon)
axis(xmax=duration/ms)

show()

