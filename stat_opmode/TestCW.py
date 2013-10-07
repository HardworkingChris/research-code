from brian import *
import ConstrainedWiener as cw
from scipy.special import erfc

sigma_units = mV/sqrt(ms)
N = 5

if __name__ == '__main__':
    S = 10*mV
    T = 40*ms
    pif_eq = Equations('''
            dx/dt = drift + sigma*xi : volt
            drift : volt/second
            sigma : volt/sqrt(second)
            ''')
    pif_ng = NeuronGroup(N, pif_eq)#, threshold='x>=10*mV', reset='x=0*mV')
    pif_ng.x = [0*mV]*N
    pif_ng.drift = [1*mV/ms]*N
    pif_ng.sigma = [sqrt(1*mV**2/ms),
            sqrt(4*mV**2/ms),
            sqrt(6*mV**2/ms),
            sqrt(9*mV**2/ms),
            sqrt(15*mV/sqrt(ms))]

    @network_operation
    def calc_drift():
        mu = 1*mV/ms
        ss = pif_ng.sigma
        xx = [0]*N
        t = defaultclock.t
        drifts = []
        for x,sigma in zip(xx, ss):
            x *= volt
            sigma = float(sigma/sigma_units)*sigma_units
            d_i = cw.constrained_wiener_drift(x, t, mu, sigma, S, T)
            drifts.append(d_i)
        pif_ng.drift = drifts
        return

    x_mon = StateMonitor(pif_ng, 'x', record=True)
    drift_mon = StateMonitor(pif_ng, 'drift', record=True)
    Smon = SpikeMonitor(pif_ng)
    print("Running")
    run(T)
    ion()
    plot(x_mon.times, transpose(x_mon.values))
    legend(["$\sigma^2$: %2.1f $mV^2/ms$" % ((s/sigma_units)**2)\
            for s in pif_ng.sigma], loc='best')
    plot([0, defaultclock.t], [S, S], 'k--')
    figure()
    plot(drift_mon.times, transpose(drift_mon.values))
    legend(["$\sigma^2$: %2.1f $mV^2/ms$" % ((s/sigma_units)**2)\
            for s in pif_ng.sigma], loc='best')

    #show()

