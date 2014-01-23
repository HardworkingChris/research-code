from brian import *
from scipy.special import erfc

def constrained_wiener_drift(x, t, mu, sigma, S, T):
    '''
    Calculates the time-dependent drift of a Wiener process constrained to
    stay below `S` up to time `T` with base drift `mu` and noise `sigma`,
    at (x,t).
    '''
    density = (1 - 0.5*erfc((S-x-mu*(T-t))/(sigma*sqrt(2*(T-t))))
            - 0.5*exp((2*mu*(S-x))/(sigma**2))
            * erfc((S-x+mu*(T-t))/(sigma*sqrt(2*(T-t)))))
    partdiff = (- 1 / (sigma*sqrt(2*pi*(T-t)))
            * exp(-((S-x-mu*(T-t))/(sigma*sqrt(2*(T-t))))**2)
            + (mu/(sigma**2))*exp((2*mu*(S-x))/(sigma**2))
            * erfc((S-x+mu*(T-t))/(sigma*sqrt(2*(T-t))))
            - (1/(sigma*sqrt(2*pi*(T-t))))
            * exp((2*mu*(S-x))/(sigma**2))
            * exp(-((S-x+mu*(T-t))/(sigma*sqrt(2*(T-t))))**2))
    drift = mu+((sigma**2)/density)*partdiff
    return drift


