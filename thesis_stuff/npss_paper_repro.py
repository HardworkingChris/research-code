"""
Reproduction of main results.
"""
from brian import (Network, NeuronGroup, SpikeMonitor, StateMonitor,
                   Connection, defaultclock, clear,
                   mV, second, Hz, ms)
import gc
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
import itertools as itt
import spikerlib as sl
import pickle


fflock = mp.Lock()
dflock = mp.Lock()
FREQUENCY_FILE = "pkl/calibratedfreq.pkl"
NPSS_FILE = "pkl/npssresults.pkl"

def load_or_calibrate(nrndef, Nin, weight, sync, fout,
                      Vth=15*mV, tau=10*ms):
    nrndeftuple = tuple(nrndef.items())
    key = (nrndeftuple, Nin, weight, tuple(sync), fout, Vth, tau)
    fflock.acquire()
    try:
        with open(FREQUENCY_FILE) as freqfile:
            filedata = pickle.load(freqfile)
    except IOError:
        filedata = {}
    finally:
        fflock.release()
    fin = filedata.get(key, None)
    if fin is None:
        print("Calibrating {} {} {}".format(Nin, weight, fout))
        fin = sl.tools.calibrate_frequencies(nrndef, Nin, weight, sync,
                                             fout, Vth=15*mV, tau=10*ms)
        fflock.acquire()
        try:
            with open(FREQUENCY_FILE, 'r') as freqfile:
                filedata = pickle.load(freqfile)
        except IOError:
            filedata = {}
        finally:
            with open(FREQUENCY_FILE, 'w') as freqfile:
                filedata[key] = fin
                pickle.dump(filedata, freqfile)
            fflock.release()
    return fin

def save_data(key, npss):
    dflock.acquire()
    try:
        with open(NPSS_FILE, 'r') as npssfile:
            filedata = pickle.load(npssfile)
    except IOError:
        filedata = {}
    finally:
        with open(NPSS_FILE, 'w') as npssfile:
            filedata[key] = npss  # don't care if overwriting existing item
            pickle.dump(filedata, npssfile)
            print("Saved NPSS data for: {} {} {}".format(key[1], key[2], key[4]))
        dflock.release()

def runsim(Nin, weight, fout, sync):
    sim = Network()
    clear(True)
    gc.collect()
    defaultclock.reinit()
    duration = 5*second
    lifeq = "dV/dt = -V/(10*ms) : volt"
    nrndef = {"model": lifeq, "threshold": "V>=15*mV", "reset": "V=0*mV",
              "refractory": 2*ms}
    fin = load_or_calibrate(nrndef, Nin, weight, sync, fout,
                            Vth=15*mV, tau=10*ms)
    # print("Calibrated frequencies:")
    # print(", ".join(str(f) for f in fin))
    inputgroups = []
    connections = []
    neurons = []
    Nneurons = len(fin)
    neurons = NeuronGroup(Nneurons, **nrndef)
    for idx in range(Nneurons):
        fin_i = fin[idx]
        sync_i, sigma_i = sync[idx]
        inputgrp = sl.tools.fast_synchronous_input_gen(Nin, fin_i,
                                                       sync_i, sigma_i,
                                                       duration)
        defaultclock.reinit()
        conn = Connection(inputgrp, neurons[idx], state="V", weight=weight)
        inputgroups.append(inputgrp)
        connections.append(conn)
    voltagemon = StateMonitor(neurons, "V", record=True)
    spikemon = SpikeMonitor(neurons, record=True)
    sim.add(neurons, voltagemon, spikemon)
    sim.add(*inputgroups)
    sim.add(*connections)
    print("Running {} {} {}".format(Nin, weight, fout))
    sim.run(duration, report="stdout")
    mnpss = []
    allnpss = []
    for idx in range(Nneurons):
        vmon = voltagemon[idx]
        smon = spikemon[idx]
        # print("Desired firing rate: {}".format(fout))
        # print("Actual firing rate:  {}".format(len(smon)/duration))
        if len(smon) > 0:
            npss = sl.tools.npss(vmon, smon, 0*mV, 15*mV, 10*ms, 2*ms)
        else:
            npss = 0
        mnpss.append(np.mean(npss))
        allnpss.append(npss)
    nrndeftuple = tuple(nrndef.items())
    key = (nrndeftuple, Nin, weight, tuple(sync), fout, 15*mV, 10*ms)
    save_data(key, allnpss)
    imshape = (len(sigma), len(Sin))
    imextent = (0, 1, 0, 4.0)
    mnpss = np.reshape(mnpss, imshape, order="F")
    plt.figure()
    plt.imshow(mnpss, aspect="auto", origin="lower", extent=imextent,
               interpolation="none", vmin=0, vmax=1)
    cbar = plt.colorbar()
    cbar.set_label("$\overline{M}$")
    plt.xlabel("$S_{in}$")
    plt.ylabel("$\sigma_{in}$ (ms)")
    filename = "npss_{}_{}_{}".format(Nin, weight, fout).replace(".", "")
    plt.savefig(filename+".pdf")
    plt.savefig(filename+".png")
    print("{} saved".format(filename))
    voltages = voltagemon.values
    spiketrains = spikemon.spiketimes.values()
    pickle.dump({"voltages": voltages, "spiketrains": spiketrains},
                 open(filename+".pkl", 'w'))
    return voltagemon, spikemon


Nin = [100, 50, 60, 60, 200, 60]
weight = [0.1*mV, 0.2*mV, 0.3*mV, 0.5*mV, 0.1*mV, 0.5*mV]
fout = [5*Hz, 100*Hz, 10*Hz, 70*Hz, 10*Hz, 100*Hz]
Sin = np.arange(0, 1.01, 0.1)
sigma = np.arange(0, 4.1, 0.5)*ms
syncconf = [(s, j) for s, j in itt.product(Sin, sigma)]

configurations = []
for n, w, f in zip(Nin, weight, fout):
    configurations.append({"Nin": n, "weight": w, "fout": f, "sync": syncconf})

pool = mp.Pool()
print("Building pool")
mppool = [pool.apply_async(runsim, kwds=c) for c in configurations]
print("Getting results")
results = [res.get() for res in mppool]

# for conf in configurations:
#     runsim(**conf)
