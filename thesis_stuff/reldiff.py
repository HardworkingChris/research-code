from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


Vth = 15  # mV
w = 2     # ms
tau = 10  # ms

def calc_error(isi):
    """
    Calculate approximation error for a given target inter-spike interval.
    """

    # input current required for LIF to spike at t = isi
    current = Vth/(tau*(1-np.exp(-isi/tau)))

    # membrane potential of LIF at time (isi-w)
    lif = current*tau*(1-np.exp(-(isi-w)/tau))
    # membrane potential of approximate model at time (isi-w)
    approx = current*(isi-w)

    return abs(lif-approx)/lif

def calc_bound_diff(isi):
    """
    Calculate ratio  of Lower bound over Upper bound as a function of ISI.
    Total reset neuron only.
    """
    upper = Vth/w  # mV/ms

    inp = Vth/(1-np.exp(-isi/tau))
    lower = (Vth-inp*(1-np.exp(-(isi-w)/tau)))/w
    return lower/upper

isirange = np.arange(2.001, 20, 0.001)
errors = [calc_error(isi) for isi in isirange]
plt.figure(figsize=(4,3))
plt.plot(isirange, errors)
pointsx = [1000/70, 1000/100, 1000/400]  # 70, 100, 400 Hz
pointsy = [calc_error(x) for x in pointsx]
for x, y in zip(pointsx, pointsy):
    plt.plot(x, y, 'k.', markersize=10)
    plt.annotate("{} Hz".format(int(1000/x)), xy=(x, y),
                 xytext=(x-2, y+0.1))
plt.axis(xmin=0)
locs, labels = plt.xticks()
locs = np.append(locs, 2)
plt.xticks(locs)
plt.xlabel("$\Delta t_i$ (ms)")
plt.ylabel("d")

plt.subplots_adjust(bottom=0.17, top=0.95, left=0.2, right=0.95)
plt.savefig("figures/relerr.pdf")

bound_diff = [calc_bound_diff(isi) for isi in isirange]
plt.figure(figsize=(4,3))
plt.plot(isirange, bound_diff)
pointsx = [1000/70, 1000/100, 1000/400]  # 70, 100, 400 Hz
pointsy = [calc_bound_diff(x) for x in pointsx]
for x, y in zip(pointsx, pointsy):
    plt.plot(x, y, 'k.', markersize=10)
    plt.annotate("{} Hz".format(int(1000/x)), xy=(x, y),
                 xytext=(x+0.5, y+0.01))
plt.plot([w, w], [0, max(bound_diff)], "k--")
plt.axis(xmin=0)
locs, labels = plt.xticks()
locs = np.append(locs, w)
plt.xticks(locs)
plt.xlabel("$\Delta t_i$ (ms)")
plt.ylabel("Bound ratio $(\\frac{L}{U})$")

plt.subplots_adjust(bottom=0.17, top=0.95, left=0.2, right=0.95)
plt.savefig("figures/bound_ratio.pdf")
