from brian import *
import sys
import gc

def morrislecar():
    '''
    Model equations and initial parameters are taken from Izhikevich, 2004
    '''
    clear(True)
    gc.collect()
    reinit_default_clock()

    'Tuning parameter'
    V_1 = 0*mV
    V_2 = 15*mV
    V_3 = 10*mV
    V_4 = 10*mV

    C = 20*ufarad

    'Conductances'
    g_Ca = 4*msiemens
    g_K = 8*msiemens
    g_L = 2*msiemens

    'Equilibrium potentials'
    V_K = -70*mV
    V_L = -50*mV
    V_Ca = 100*mV

    l = 0.1/second

    eqs=Equations('dV/dt = ('
#                        'I'
                        '- g_L*(V-V_L)'
                        '- g_Ca*M_ss*(V-V_Ca)'
                        '- g_K*N*(V-V_K))'
                        '/C '
                        ': volt')
#    eqs+=Equations('I : amp ')
    eqs+=Equations('dN/dt = lV * (N_ss - N) : 1')
    eqs+=Equations('M_ss = (1+tanh((V-V_1)/V_2))/2 : 1')
    eqs+=Equations('N_ss = (1+tanh((V-V_3)/V_4))/2 : 1')
    eqs+=Equations('lV = l*cosh((V-V_3)/(2*V_4)) : 1/second')
    eqs.prepare()
    nrns = NeuronGroup(1, eqs)
    I = PoissonGroup(100, 30*Hz)
    con = Connection(I, nrns, 'V')
    con[:,0] = 0.5*mV
    nrns.V = -50*mV
    V_mon = StateMonitor(nrns, 'V', record=True)
    N_mon = StateMonitor(nrns, 'N', record=True)
    run(200*ms)
    return V_mon

if __name__=='__main__':
    mems = morrislecar()
    for v in mems:
        plot(mems.times, v)
    show()
