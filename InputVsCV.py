from brian import *
import time
import sys
if __name__=='__main__':
    duration = 2000*ms
    max_allowed_sims = 400
    savelocation = '/home/achilleas/Documents/Uni/working_dir/simout.py/tmp/'

    input_freqs = arange(100,401,25)
    input_num_sts = arange(40,101,10)
    input_volts = arange(0.1,0.21,0.05)
    numsims = len(input_freqs)*len(input_num_sts)*len(input_volts)
    numinputgens = len(input_freqs)*sum(input_num_sts)*len(input_volts) 
    numconnections = numinputgens
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
connections' % (numsims, numinputgens, numconnections))

    config_start = time.time()
    V_reset = 13.65*mV
    V_th = 15*mV
    V_rest = 0*mV
    tau_mem = 10*ms
    refr = 0.1*ms
    eqs = Equations('dV/dt = (-V+V_rest)/tau_mem : volt')
    nrns = NeuronGroup(numsims,eqs,reset=V_reset,threshold='V>V_th',\
            refractory=refr)
    generator_rates = array([])
    configs = [] # list of configurations
    for gn in input_num_sts:
        for grate in input_freqs:
            for gv in input_volts:
                generator_rates = append(generator_rates, ones(gn)*grate)
                configs.append([gn, grate, gv])
    inp = PoissonGroup(numinputgens, generator_rates*Hz)
    con_matrix = zeros([numconnections, numsims])
    nrn = 0
    con = 0
    for c,nrn in zip(configs, range(numsims)):
        # c is a list: [n_inputs, input_rate, input_voltage]
        con_matrix[con:con+c[0], nrn] = ones(c[0])*c[2]
        con += c[0]
    cons = Connection(source=inp,target=nrns,state='V',weight=con_matrix*mV)
    out_mon = SpikeMonitor(nrns)
    mem_mon = StateMonitor(nrns,'V',record=True)
    config_end = time.time()
    config_dura = (config_end-config_start)*second
    print "Simulation configuration completed in %s"\
            % config_dura
    print "Running",numsims,"simulations ..."
    run(duration,report='stdout')
    print "Done. Preparing results ..."
    f_in = input_freqs
    numspikes = zeros(numsims)
    mean_isi = zeros(numsims)
    std_isi = zeros(numsims)
    for nrn in out_mon.spiketimes.iterkeys():
        nrnspikes = out_mon.spiketimes[nrn]
        numspikes[nrn] = len(nrnspikes)
        if numspikes[nrn] > 2:
            isi = diff(nrnspikes)
            mean_isi[nrn] = mean(isi)
            std_isi[nrn] = std(isi)
        else:
            mean_isi[nrn] = 1e-10 # to avoid division by zero in CV calculation
            std_isi[nrn] = 0 

    f_out = numspikes/duration
    cv = std_isi/mean_isi
#    print "Configuration\tCV"
#    nrn = 0
#    for con, var, misi in zip(configs, cv, mean_isi):
#        print "Conf: %s, CV: %f, Mean ISI: %s" % (con, var, misi*second)
    t = arange(0.002,max(mean_isi),0.0001)
    theo_cv = sqrt((t-0.002)/t)

