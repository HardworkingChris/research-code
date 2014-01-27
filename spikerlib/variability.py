import numpy as __np


def CV(spiketrain):
    '''
    Calculates the coefficient of variation for a spike train or any supplied
    array of values

    Parameters
    ----------
    spiketrain : numpy array (or arraylike)
        A spike train characterised by an array of spike times

    Returns
    -------
    CV : float
        Coefficient of variation for the supplied values

    '''

    isi = __np.diff(spiketrain)
    if len(isi) == 0:
        return 0.0

    avg_isi = __np.mean(isi)
    std_isi = __np.std(isi)
    return std_isi/avg_isi


def CV2(spiketrain):
    '''
    Calculates the localised coefficient of variation for a spike train or
    any supplied array of values

    Parameters
    ----------
    spiketrain : numpy array (or arraylike)
        A spike train characterised by an array of spike times

    Returns
    -------
    CV2 : float
        Localised coefficient of variation for the supplied values

    '''

    isi = __np.diff(spiketrain)
    N = len(isi)
    if (N == 0):
        return 0

    mi_total = 0
    for i in range(N-1):
        mi_total = mi_total + abs(isi[i]-isi[i+1])/(isi[i]+isi[i+1])

    return mi_total*2/N


def IR(spiketrain):
    '''
    Calculates the IR measure for a spike train or any supplied array of values

    Parameters
    ----------
    spiketrain : numpy array (or arraylike)
        A spike train characterised by an array of spike times

    Returns
    -------
    IR : float
        IR measure for the supplied values

    '''



    isi = __np.diff(spiketrain)
    N = len(isi)
    if (N == 0):
        return 0

    mi_total = 0
    for i in range(N-1):
        mi_total = mi_total + abs(__np.log(isi[i]/isi[i+1]))

    return mi_total*1/(N*__np.log(4))


def LV(spiketrain):
    '''
    Calculates the measure of local variation for a spike train or any
    supplied array of values

    Parameters
    ----------
    spiketrain : numpy array (or arraylike)
        A spike train characterised by an array of spike times

    Returns
    -------
    LV : float
        Measure of local variation for the supplied values

    '''


    isi = __np.diff(spiketrain)
    N = len(isi)
    if (N == 0):
        return 0

    mi_total = 0
    for i in range(N-1):
        mi_total = mi_total + ((isi[i] - isi[i+1])/(isi[i] + isi[i+1]))**2

    return mi_total*3/N


def SI(spiketrain):
    '''
    Calculates the SI measure for a spike train or any supplied array of values

    Parameters
    ----------
    spiketrain : numpy array (or arraylike)
        A spike train characterised by an array of spike times

    Returns
    -------
    SI : float
        SI measure for the supplied values

    '''


    isi = __np.diff(spiketrain)
    N = len(isi)
    if (N == 0):
        return 0

    mi_sum = 0
    for i in range(N-1):
        mi_sum = mi_sum + __np.log(4*isi[i]*isi[i+1]/((isi[i]+isi[i+1])**2))

    return -1./(2*N*(1-__np.log(2)))*mi_sum
