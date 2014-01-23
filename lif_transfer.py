from brian import *
import time

if __name__=='__main__':
    input_freqs = arange(200,450,0.5)
    n_inputs = 50
    numsims = len(input_freqs)
    duration = 2000*ms
    v_reset = '''
    v = 13.65*mV
    v_th = 15*mV
    '''
    v_rest = 0*mV
    tau_mem = 10*ms
    refr = 2*ms
    eqs = Equations('''
    dv/dt = (-v+v_rest)/tau_mem : volt
    dv_th/dt = (-v_th+15*mV)/msecond : volt    
    ''')
#    dv_th/dt = -(exp(-(v_th/mV)**2)*sqrt(exp((v_th/mV)**2))*v_th)/(sqrt(2*pi)*ms) : volt
    DV_s = 0.16*mV
    nrns = NeuronGroup(numsims,eqs,reset=v_reset,threshold='v>v_th',refractory=refr)
    nrns.v_th = 15*mV
    rates = array([])
    for f_in in input_freqs:
        rates = append(rates,ones(n_inputs)*f_in)
    inp = PoissonGroup(n_inputs*numsims,rates)
    con_matrix = zeros([n_inputs*numsims,numsims])
    for i in range(numsims):
        con_matrix[i*n_inputs:(i+1)*n_inputs,i] = ones(n_inputs)*DV_s
    cons = Connection(source=inp,target=nrns,state='v',weight=con_matrix)
#    inp_mon = SpikeMonitor(inp)
#    mem_mon = StateMonitor(nrns,'v',record=True)
#    thr_mon = StateMonitor(nrns,'v_th',record=True)
    out_mon = SpikeMonitor(nrns)
    print "Running",numsims,"simulations ..."
    run(duration,report='stdout')
#    for i in range(numsims):
#        hold(True)
#        plot(mem_mon.times,mem_mon[i])
#        plot(thr_mon.times,thr_mon[i])
#        show()
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

        

