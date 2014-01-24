import numpy as np


def mean_pairwise_vp_st_distance(all_spikes, cost):
    count = len(all_spikes)
    distances = []
    for i in range(count - 1):
        for j in range(i + 1, count):
            dist = vp_st_distance(all_spikes[i], all_spikes[j], cost)
            distances.append(dist)
    return np.mean(distances)


def vp_st_distance(spiketrain_a, spiketrain_b, cost):
    num_spike_i = len(spiketrain_a)
    num_spike_j = len(spiketrain_b)
    if num_spike_i == 0 or num_spike_j == 0:
        return 0
    matrix = np.zeros((num_spike_i, num_spike_j))
    for i in range(num_spike_i):
        matrix[i][0] = i
    for i in range(num_spike_j):
        matrix[0][i] = i
    for m in range(1, num_spike_i):
        for l in range(1, num_spike_j):
            cost_a = matrix[m - 1][l] + 1
            cost_b = matrix[m][l - 1] + 1
            temp = abs((spiketrain_a[m]) - (spiketrain_b[l]))
            cost_c = matrix[m - 1][l - 1] + (cost * temp)
            matrix[m][l] = min(cost_a, cost_b, cost_c)
    d_spike = matrix[num_spike_i - 1][num_spike_j - 1]
    return d_spike


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

