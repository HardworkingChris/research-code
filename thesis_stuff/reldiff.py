from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def calc_error(isi):
    """
    Calculate approximation error for a given target inter-spike interval.
    """
    Vth = 15  # mV
    w = 2     # ms
    tau = 10  # ms

    # input current required for LIF to spike at t = isi
    current = Vth/(tau*(1-np.exp(-isi/tau)))

    # membrane potential of LIF at time (isi-w)
    lif = current*tau*(1-np.exp(-(isi-w)/tau))
    # membrane potential of approximate model at time (isi-w)
    approx = current*(isi-w)

    return abs(lif-approx)/lif

isirange = np.arange(2.001, 20, 0.001)
errors = [calc_error(isi) for isi in isirange]
plt.figure()
plt.plot(isirange, errors)
pointsx = [1000/70, 1000/100, 1000/400]  # 70, 100, 400 Hz
pointsy = [calc_error(x) for x in pointsx]
for x, y in zip(pointsx, pointsy):
    plt.plot(x, y, 'k.', markersize=10)
    plt.annotate("{} Hz".format(int(1000/x)), xy=(x, y),
                 xytext=(x-2, y))
plt.axis(xmin=0)
locs, labels = plt.xticks()
locs = np.append(locs, 2)
plt.xticks(locs)
plt.xlabel("$\Delta t_i$ (ms)")
plt.ylabel("d")

plt.savefig("relerr.pdf")
plt.savefig("relerr.png")
