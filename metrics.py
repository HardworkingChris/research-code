import numpy as np
import multiprocessing
import itertools


def mean_pairwise_vp_st_distance(all_spikes, cost):
    count = len(all_spikes)
    distances = []
    for i in range(count - 1):
        for j in range(i + 1, count):
            dist = vp_st_distance(all_spikes[i], all_spikes[j], cost)
            distances.append(dist)
    return np.mean(distances)


def vp_st_distance(st_one, st_two, cost):
    '''
    Calculates the "spike time" distance (Victor & Purpura, 1996) for a single
    cost.

    tli: vector of spike times for first spike train
    tlj: vector of spike times for second spike train
    cost: cost per unit time to move a spike

    Translated to Python by Achilleas Koutsou from Matlab code by Daniel Reich.
    '''
    len_one = len(st_one)
    len_two = len(st_two)
    if cost == 0:
        dist = np.abs(len_one-len_two)
        return dist
    elif cost == float('inf'):
        dist = len_one+len_two
        return dist
    scr = np.zeros((len_one+1, len_two+1))
    scr[:,0] = np.arange(len_one+1)
    scr[0,:] = np.arange(len_two+1)
    if len_one and len_two:
        for i in range(1, len_one+1):
            for j in range(1, len_two+1):
                scr[i,j]=np.min((scr[i-1,j]+1,
                                scr[i,j-1]+1,
                                scr[i-1,j-1]+cost*np.abs(st_one[i-1]-st_two[j-1]))
                               )
    return scr[-1,-1]


def interval_VP(inputspikes, outputspikes, cost, dt=0.1*ms):
    dt = float(dt)
    vpdists = []
    for prv, nxt in zip(outputspikes[:-1], outputspikes[1:]):
        interval_inputs = []
        for insp in inputspikes:
            interval_inputs.append(insp[(prv < insp) & (insp < nxt+dt)])
        vpd = mean_pairwise_distance(interval_inputs, cost)
        vpdists.append(vpd)
    return vpdists


def interval_Kr(inputspikes, outputspikes, dt=0.1*ms):
    dt = float(dt)
    krdists = []
    for prv, nxt in zip(outputspikes[:-1], outputspikes[1:]):
        krd = multivariate_spike_distance(inputspikes, prv, nxt+dt, 1)
        krdists.append(krd[1])
    return krdists


def interval_corr(inputspikes, outputspikes, b=0.1*ms, duration=None):
    b = float(b)
    corrs = []
    for prv, nxt in zip(outputspikes[:-1], outputspikes[1:]):
        interval_inputs = []
        for insp in inputspikes:
            interval_spikes = insp[(prv < insp) & (insp <= nxt)]-prv
            if len(interval_spikes):
                interval_inputs.append(interval_spikes)
        corrs_i = mean(corrcoef_spiketrains(interval_inputs, b, duration))
        corrs.append(corrs_i)
    return corrs

