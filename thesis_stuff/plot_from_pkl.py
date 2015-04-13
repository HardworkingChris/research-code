import numpy as np
import matplotlib.pyplot as plt
import pickle

NPSS_FILE = "npssresults.pkl"

try:
    with open(NPSS_FILE, 'r') as npssfile:
        filedata = pickle.load(npssfile)
except IOError:
    filedata = {}

interpolations = ["none", "nearest", "bilinear", "bicubic", "spline16",
                  "spline36", "hanning", "hamming", "hermite", "kaiser",
                  "quadric", "catrom", "gaussian", "bessel", "mitchell",
                  "sinc", "lanczos"]

for k in filedata.keys():
    nrndeftuple, Nin, weight, syncconf, fout, Vth, tau = k
    # skip simulations that had no refractory period
    refr = False
    for item in nrndeftuple:
        if "refractory" in item:
            refr = True
    if not refr:
        continue
    print(nrndeftuple)
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
    for interpol in interpolations:
        plt.clf()
        plt.imshow(mnpss, aspect="auto", origin="lower", extent=imextent,
                   interpolation=interpol, vmin=0, vmax=1)
        cbar = plt.colorbar()
        cbar.set_label("$\overline{M}$")
        plt.xlabel("$S_{in}$")
        plt.ylabel("$\sigma_{in}$ (ms)")
        filename = "npss_{}_{}_{}_{}".format(Nin, weight, fout,
                                             interpol).replace(".", "")
        plt.savefig(filename+".pdf")
        plt.savefig(filename+".png")
        print("{} saved".format(filename))
