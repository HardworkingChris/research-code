from brian import *
import time

if __name__=='__main__':

    savelocation = '/home/achilleas/Documents/Uni/working_dir/simout.py/tmp/'

    input_freqs = arange(300,400,10)
    n_inputs = 50
    numsims = len(input_freqs)
    duration = 2000*ms
    V_reset = 13.65*mV
    V_th = 15*mV
    V_rest = 0*mV
    V2_rest = 0*mV
    tau_mem = 10*ms
    tau_den = 10*ms
    capa = 1*ufarad
    capa2 = 1*ufarad
    resi = 10*kohm
    resi2 = 10*kohm
    junc_res = 1*kohm
    tau_den = capa2*resi2
    tau_mem = capa*resi
    refr = 2*ms
    eqs = Equations('''
    dV2/dt = (-V2+V2_rest)/tau_den + (V-V2)/(junc_res*capa2) : volt
    dV/dt = (-V+V_rest)/tau_mem + (V2 - V)/(junc_res*capa) : volt
    ''')
    DV_s = 0.16*mV
    nrns = NeuronGroup(numsims,eqs,reset=V_reset,threshold='V>V_th',refractory=refr)
    generator_rates = array([])
    for grate in input_freqs:
        generator_rates = append(generator_rates,ones(n_inputs)*grate)
    inp = PoissonGroup(n_inputs*numsims,generator_rates)
    con_matrix = zeros([n_inputs*numsims,numsims])
    for nrn in range(numsims):
        con_matrix[nrn*n_inputs:(nrn+1)*n_inputs,nrn] = ones(n_inputs)*DV_s
    cons = Connection(source=inp,target=nrns,state='V2',weight=con_matrix)
    out_mon = SpikeMonitor(nrns)
    count_mon = SpikeCounter(nrns)
    mem_mon = StateMonitor(nrns,'V',record=True)
    den_mon = StateMonitor(nrns,'V2',record=True)
    print "Running",numsims,"simulations ..."
    run(duration,report='stdout')
    print "Simulations DONE!"
#    for nrn in range(numsims):
#        clf()
#        figure(figsize=(15,12))
#        hold(True)
#        plot(den_mon.times,den_mon[nrn]/mV,color=(0,0,1,0.3))
#        plot(mem_mon.times,mem_mon[nrn]/mV,color=(1,0,0,1))
#        xlabel('Time (s)')
#        ylabel('Potential (mV)')
#        legend(('Dendritic potential','Somatic potential'))
#        title('''
#        V_reset: %s, V_th: %s, V_rest: %s, V2_rest: %s, tau_mem: %s,
#        tau_den: %s, C_soma: %s, C_den: %s. R_soma: %s, R_den: %s,
#        f_in: %s Hz, f_out: %s Hz
#        ''' % (V_reset, V_th, V_rest, V2_rest, tau_mem, tau_den, capa,\
#        capa2, resi, resi2, input_freqs[nrn]*Hz, count_mon.count[nrn]/duration))
#        figname = '%sinp%sHz.png' % (savelocation, input_freqs[nrn])
#        savefig(figname)
#        print 'Saved %s' % figname

    transfer = np.zeros([numsims,2])
    variability = np.zeros([numsims,2])
    print "Done. Preparing plots ..."
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

    f_out = numspikes/duration
    cv = std_isi/mean_isi
    variability = array([mean_isi, cv])
    transfer = array([f_in, f_out])
    subplot(2,1,1)
    hold(True)
    plot(transfer[0,:], transfer[1,:],'.')
    xlabel('f_in (Hz)')
    ylabel('f_out (Hz)')
    hold(False)
    subplot(2,1,2)
    hold(True)
    t = arange(0.002,max(mean_isi),0.0001)
    theo_cv = sqrt((t-0.002)/t)
    plot(t,theo_cv) # theoretical cv curve
    plot(variability[0,:], variability[1,:],'.')
    xlabel('mean ISI')
    ylabel('CV')
    show()



