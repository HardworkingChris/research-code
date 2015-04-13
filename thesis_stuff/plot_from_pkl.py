import numpy as np
import matplotlib.pyplot as plt
import pickle

NPSS_FILE = "npssresults.pkl"

try:
    with open(NPSS_FILE, 'r') as npssfile:
        filedata = pickle.load(npssfile)
except IOError:
    filedata = {}

for k in filedata.keys():
    nrndeftuple, Nin, weight, syncconf, fout, Vth, tau = k
    allnpss = filedata[k]
    mnpss = np.array([np.mean(an) for an in allnpss])
    Sin = [sc[0] for sc in syncconf]
    Sin = set(Sin)
    sigma = [sc[1] for sc in syncconf]
    sigma = set(sigma)
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
