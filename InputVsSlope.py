from brian import *
import time
import sys
import neurotools as nt

if __name__=='__main__':
    duration = 100*ms
    max_allowed_sims = 500
    savelocation = '/home/achilleas/Documents/Uni/working_dir/simout.py/tmp/'

    input_freqs = linspace(200, 400, 1)
    input_num_sts = array(linspace(40, 100, 1),dtype=int)
    input_volts = linspace(0.1, 0.5, 1)
    synchrony = linspace(0, 1, 6)
    jitter = linspace(0, 2, 5)
    numsims = len(input_freqs)*len(input_num_sts)*len(input_volts)*\
            len(synchrony)*len(jitter)
    numinputsts = len(input_freqs)*sum(input_num_sts)*len(input_volts)*\
            len(synchrony)*len(jitter)
    numconnections = numinputsts
    if numsims > max_allowed_sims:
        ans = None
        while ans != 'y' and ans != 'n' and ans != '':
            ans = raw_input('The number of simulations is very large \
(%d > %d). This may make the script (or even the entire system) unresponsive. \
\nAre you sure you want to continue? [y/N] ' % (numsims, max_allowed_sims))
            ans = ans.lower()

        if ans == 'n' or ans == '':
            sys.exit("Exiting.")
    print('Building %d simulations with %d input spike trains and %d \
connections' % (numsims, numinputsts, numconnections))

    config_start = time.time()
    V_reset = 0*mV
    V_th = 15*mV
    V_rest = 0*mV
    tau_mem = 10*ms
    refr = 2*ms
    eqs = Equations('dV/dt = (-V+V_rest)/tau_mem : volt')
    nrns = NeuronGroup(numsims,eqs,reset=V_reset,threshold='V>V_th',\
            refractory=refr)
    inp_spiketrains = []
    configs = [] # list of configurations
    for n in input_num_sts:
        for r in input_freqs:
            for v in input_volts:
                for s in synchrony:
                    for j in jitter:
                        inp_spiketrains.extend(nt.sync_inp(n, s, j, r,\
                                duration))
                        configs.append([n, r*Hz, v*mV, s, j*ms])
                        percent = len(configs)*100/numsims
                        print "%d/%d (%d%%)\r" %\
                                (len(configs), numsims, percent),
                        sys.stdout.flush()
    inp = MultipleSpikeGeneratorGroup(inp_spiketrains)
    con_matrix = zeros([numconnections, numsims])
    nrn = 0
    con = 0
    for c,nrn in zip(configs, range(numsims)):
        # c is a list: [n_inputs, input_rate, input_voltage, synchrony, jitter]
        con_matrix[con:con+c[0], nrn] = ones(c[0])*c[2]
        con += c[0]
    if con != numconnections:
        sys.exit("Something went wrong. Counted %d connections instead of %d"\
                % (con, numconnections))
    cons = Connection(source=inp, target=nrns, state='V', weight=con_matrix*mV)
    inp_mon = SpikeMonitor(inp)
    out_mon = SpikeMonitor(nrns)
    mem_mon = StateMonitor(nrns,'V',record=True)
    config_end = time.time()
    config_dura = (config_end-config_start)*second
    print "Simulation configuration completed in %s"\
            % config_dura
    print "Running",numsims,"simulations ..."
    run(duration, report='stdout')
    print "Done. Preparing results ..."
    M = np.zeros(numsims)
    for nrn in out_mon.spiketimes.iterkeys():
        # pre-spike slope
        m_slope, slopes = nt.npss(mem_mon[nrn], out_mon[nrn], V_th, 2*ms)
        M[nrn] = m_slope

