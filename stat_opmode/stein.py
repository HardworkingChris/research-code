'''
Run as follows:
    python Stein.py <data directory name>

Suffix `.data` will be appended to the directory name.
If data has already been generated, the analysis can be run as follows:
    python Stein.py <data directory name> --no-run


TODO:
    We could run several simulations in the same lifsim() function by defining
    a multi neuron NeuronGroup and feeding each neuron with it's own inputs,
    instead of one neuron per function. This would be much faster to run.
    The data iterator as well as the return data would have to be changed for
    this.
'''
from brian import *
from brian.tools.datamanager import *
from brian.tools.taskfarm import *
import itertools as it
import sys
import gc
from time import time
duration = 100*ms
defaultclock.dt = dt = 0.1*ms  # simulation time step

N = 1
tau = 10*ms
thr = 10*mV
V0 = 0*mV
trefr = 0*ms

w = 2*ms  # window
w_dt = int(w/dt)  # window as number of simulation time steps

def lifsim(exc_weight, exc_rate, inh_weight, inh_rate, report):
    'Garbage collection: needed when running many simulations in parallel'
    clear(True)
    gc.collect()
    reinit_default_clock()
    'Random seed: Could store these for reproducing exact behaviour'
    np.random.seed(int(time()+(exc_weight+exc_rate+inh_weight+inh_rate)*1e5))
    'Give units to parameters'
    exc_weight *= mV
    exc_rate *= Hz
    inh_weight *= mV
    inh_rate *= Hz

    'Set up neuron'
    eqns = 'dV/dt = (V0-V)/tau : volt'
    nrngroup = NeuronGroup(N, eqns,
            threshold='V>thr', reset=V0, refractory=trefr)
    nrngroup.V = V0
    'Set up inputs and connections'
    exc_inp = PoissonGroup(1, exc_rate)
    inh_inp = PoissonGroup(1, inh_rate)
    exc_conn = Connection(exc_inp, nrngroup, 'V')
    exc_conn[:,0] = exc_weight
    inh_conn = Connection(inh_inp, nrngroup, 'V')
    inh_conn[:,0] = inh_weight
    'Set up monitors: record membrane potential and output spikes'
    Vmon = StateMonitor(nrngroup, 'V', record=True)
    spikemon = SpikeMonitor(nrngroup)
    'Run the simulation'
    run(duration, report=report)

    'Return dictionary of parameters + results'
    return {
            'exc_weight': exc_weight,
            'exc_rate': exc_rate,
            'inh_weight': inh_weight,
            'inh_rate': inh_rate,
            'V': Vmon,
            'spikes': spikemon,
            }

def param_estimate(V, spiketimes, S, dt=0.1*ms):
    '''
    Estimates the parameters (mu, sigma) of a perfect integrator that
    approximates the membrane potential `V`.

    V: one-dimensional array-like
        Membrane potential trajectory
    spiketimes: one-dimensional array-like
        Times when spikes were fired
    S: brian units or float
        Firing threshold in volts
    refr: brian units or float
        Refractory period in seconds
    dt: brian units or float
        Simulation time step in seconds (default: 0.1 ms)

    TODO:
        - Support for multiple estimations by inputting two dimensional `V` and
          `spiketimes` arrays. Return values should be changed to account
          for this. Possibly a dictionary or 2-d array.
    '''
    isis = append(spiketimes[0], diff(spiketimes))
                                # count first spike time as first interval
    misis = mean(isis)
    st_dt = array(spiketimes/dt).astype('int')-1 # spike time bin indices
    params = []
    for st_i, isi in zip(st_dt, isis):
        mu = S/(isi*second) # biased estimator
        isi_dt = int(isi/dt)
        Visi = V[(st_i-isi_dt+2):(st_i+2)] # interval membrane potential
        dVisi = diff(Visi)
        sigma = sqrt(sum(dVisi**2)/isi)*mV/sqrt(ms)
        mu -= sigma**2 / S # remove bias
        params.append((mu, sigma))
    return params

if __name__=='__main__':
    try:
        data_dir = sys.argv[1]
    except IndexError:
        print >> sys.stderr, "ERROR: No data directory provided"
        raise
    data = DataManager(data_dir)
    print("\n")
    if '--no-run' not in sys.argv:
        'Run simulations'
        exc_weight = [5]
        exc_rate = [100, 120, 250]
        inh_weight = [-3]
        inh_rate = [50]
        params = it.product(exc_weight, exc_rate, inh_weight, inh_rate)
        nsims = len(exc_weight)*len(exc_rate)*len(inh_weight)*len(inh_rate)
        print('Simulations configured. Running ...')
        run_tasks(data, lifsim, params, gui=False, poolsize=0, numitems=nsims)
        print('Simulations done!\nData stored in %s.data directory.\n' % (
            data_dir))
    else:
        print('Skipping simulation run. Working with %s.data directory\n' % (
            data_dir))

    #numsims = data.itemcount()
    #print('Total number of simulations: %i' % numsims)

    '''
    First, let's estimate the values of mu and sigma of a perfect integrator
    that behaves as similar to the simulated neuron as possible.
    '''
    for d in data.itervalues():  # iterate configurations
        exc_weight = d.get('exc_weight')
        exc_rate = d.get('exc_rate')
        inh_weight = d.get('inh_weight')
        inh_rate = d.get('inh_rate')
        membrane = d.get('V') # StateMonitor
        dt = membrane.clock.dt
        spikes = d.get('spikes') # SpikeMonitor
        N, B = shape(membrane.values) # N: n neurons, B: duration (in bins)
        T = B*dt # T: duration (in seconds)
        print("Configuration set:\n"
                "a: %s, i: %s, lambda+: %s, lambda-: %s\n" % (
                exc_weight, inh_weight, exc_rate, inh_rate))
        for n in range(N):  # iterate simulations within configuration set
            V = membrane[n]
            spiketimes = spikes[n]
            nspikes = len(spiketimes)
            print("\tSimulation %i of %i has %i spikes" % (n+1, N, nspikes))
            if nspikes == 0:
                # no spikes; skip
                print "Skipping"
                continue
            params = param_estimate(V, spiketimes, thr, dt)
            spiketimes_dt = (spiketimes/dt).astype('int') # spike indices
            V_w = V[spiketimes_dt-w_dt] # values of V at windows
            isis = append(spiketimes[0], diff(spiketimes))
            i = 0
            for (mu, sigma), T, v_w  in zip(params, isis, V_w):
                                                    # iterate intervals
                display_in_unit(mu, mV/ms)
                display_in_unit(sigma, mV/sqrt(ms))
                print("\t\tInterval with duration %s generated coefficients "
                        "\n\t\tmu: %s, sigma: %s" % (T*second, mu, sigma))
                if T*second <= w:
                    print("\tInterval too short. Discarding!")
                    continue
                clear(True)
                gc.collect()
                reinit_default_clock()
                defaultclock.dt = dt  # simulation time step
                nsamples = 100
                Wt_eq = 'dx/dt = mu + sigma*xi : volt'
                Wt_ng = NeuronGroup(nsamples, Wt_eq)
                Wt_ng.x = 0*mV
                Wt = StateMonitor(Wt_ng, 'x', record=True)
                run(T*second)
                t = Wt.times
                T = t[-1]
                #testbt = Wt[0] - t/T*Wt[0][-1] + thr*t/T
                #plot(t, Wt[0], color='green', linestyle='--', label='W(t)')
                #plot(t, testbt, color='green', label='B(t)')
                #if i == 0:
                #    plot(t, V[0:spiketimes_dt[i]], color='blue', label='V(t)')
                #else:
                #    try:
                #        plot(t, V[spiketimes_dt[i-1]:spiketimes_dt[i]],
                #                               color='blue', label='V(t)')
                #    except ValueError:
                #        print(len(t),
                #               len(V[spiketimes_dt[i-1]:spiketimes_dt[i]]))
                #        print "*********************"
                #i += 1
                #plot([T*second-w]*2, [0, thr], color='red')
                #plot([0, T], [thr, thr], color='black', linestyle='--')
                #legend(loc='best')
                #show()
                L = 0
                for Wt_i in Wt:
                    Bt = Wt_i - t/T*Wt_i[-1] + thr*t/T
                            # Bt: brownian bridge where B(0) = 0 and
                            # B(T) = thr (threshold)
                    if Bt[-w_dt-1] < v_w:
                        L += 1
                p_value = 1.0*L/nsamples
                print("\t\tEstimated p-value: %f\n" % (p_value))
            print("")
