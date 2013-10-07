from __future__ import division
from brian import *
from brian.tools.taskfarm import *
from brian.tools.datamanager import *
import neurotools as nt
import itertools
import gc
from time import time


def hhsim(wE, wI, fS, fR, report):
    clear(True)
    gc.collect()
    reinit_default_clock()
    seed = int(time()+(wE+wI+fS+fR)*1e3)
    np.random.seed(seed)
    # Simulation parameters
    nneurons = 21
    defaultclock.dt = dt = 0.1*ms
    duration = 3*second
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
    wExc = wE*nS
    wInh = wI*nS
    syncrate = fS*Hz
    randrate = fR*Hz

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
    neurons = NeuronGroup(nneurons, eqs, threshold=threshold)#, method='RK')
    sync_inputs = []
    rand_inputs = []
    n_in = 1000
    S = linspace(0, 1, nneurons)
    for i, s in enumerate(S):
        n_sync = n_in*s
        n_rand = n_in-n_sync
        if n_sync:
            sync_inputs.append(
                    PoissonInput(neurons[i], N=1, rate=syncrate, weight=wExc,
                        state='gExc', copies=n_sync, jitter=0*second,
                        record=False)
                    )
        if n_rand:
            rand_inputs.append(
                    PoissonInput(neurons[i], N=n_rand, rate=randrate,
                        weight=wExc, state='gExc', record=False)
                    )
    inh_inputs = PoissonInput(neurons, N=n_in, rate=2*Hz, weight=wInh,
            state='gInh', record=False)
    # Init conditions
    neurons.v = -65*mV
    neurons.h = 1
    # Monitors
    memmon = StateMonitor(neurons, 'v', record=True)
    spikemon = SpikeMonitor(neurons)
    excCondMon = StateMonitor(neurons, 'gExc', record=True)
    inhCondMon = StateMonitor(neurons, 'gInh', record=True)
    # Run
    run(duration, report=None)
    # Make a 2D histogram of the membrane potential at T-w
    bins = frange(-0.07, -0.055, 1*mV)
    w = 10*ms
    slopehist = zeros((nneurons, len(bins)-1))
    i = 0
    for i, (mem, sp) in enumerate(zip(memmon, spikemon)):
        if len(sp) > 2:
            m, v, wins = nt.sta(mem, sp, w, dt)
            winstart = wins[:,0]
            h, b = histogram(winstart, bins=bins, normed=True)
            slopehist[i,:] = h
        else:
            slopehist[i,:] = zeros(len(bins)-1)
    outrates = array([len(s)/duration for s in spikemon.spiketimes.values()])
    #s_inputs = array([si.recorded_events for si in sync_inputs])
    #r_inputs = array([ri.recorded_events for ri in rand_inputs])
    #i_inputs = inh_inputs.recorded_events
    return {
            'wExc': wExc,
            'wInh': wInh,
            'syncrate': syncrate,
            'randrate': randrate,
            'outrates': outrates,
            'slopehist': slopehist,
            'bins': bins,
            'S': S,
            'mems': memmon.values,
            'spikes': spikemon.spiketimes,
            #'sync_inputs': s_inputs,
            #'rand_inputs': r_inputs,
            #'inh_inputs': i_inputs,
            'gExc': excCondMon.values,
            'gInh': inhCondMon.values,
            }

if __name__=='__main__':
    data_dir = sys.argv[1]
    data = DataManager(data_dir)
    print('\n')
    wExc = frange(2, 10, 2)
    synchrate = frange(20, 40, 5)
    randrate = frange(20, 40, 5)
    wInh = array([50, 80])
    params_prod = itertools.product(
            wExc, wInh, synchrate, randrate
            )
    nsims = len(wExc)*len(wInh)*len(synchrate)*len(randrate)
    print("Simulations configured. Running ...")
    run_tasks(data, hhsim, params_prod, gui=False, poolsize=0, numitems=nsims)
    print("Simulations done!")
    print("Data stored in %s.data" % (data_dir))


