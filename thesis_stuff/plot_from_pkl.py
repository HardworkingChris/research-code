import numpy as np
import matplotlib.pyplot as plt
import pickle

NPSS_FILE = "pkl/npssresults.pkl"

try:
    with open(NPSS_FILE, 'r') as npssfile:
        filedata = pickle.load(npssfile)
except IOError:
    filedata = {}

# interpolations = ["none", "nearest", "bilinear", "bicubic", "spline16",
#                   "spline36", "hanning", "hamming", "hermite", "kaiser",
#                   "quadric", "catrom", "gaussian", "bessel", "mitchell",
#                   "sinc", "lanczos"]
interpolations = ["hamming"]

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
    Sin = sorted(list(set(Sin)))
    sigma = [sc[1]*1000 for sc in syncconf]
    sigma = sorted(list(set(sigma)))
    imshape = (len(sigma), len(Sin))
    syncconf = [{"S": s, "J": j} for s in Sin for j in sigma]
    syncconf = np.reshape(syncconf, imshape, order="F")
    mnpss = np.reshape(mnpss, imshape, order="F")
    imextent = (0, 1, 0, 4.0)

    # PLOTTING
    plt.figure("Sin vs M", figsize=(4,3))
    plt.clf()
    plt.plot(Sin, mnpss[0], "b--", marker=".", markersize=15)
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("$S_{in}$")
    plt.ylabel("$\overline{M}$")
    plt.subplots_adjust(bottom=0.15, top=0.95, left=0.2, right=0.95)
    filename = "figures/SyncM_{}_{}_{}".format(Nin, weight, fout).replace(".", "")
    plt.savefig(filename+".pdf")
    plt.savefig(filename+".png")
    print("{} saved".format(filename))

    plt.figure("Sigma vs M", figsize=(4,3))
    plt.clf()
    plt.plot(sigma, mnpss[:,-1], "b--", marker=".", markersize=15)
    plt.plot([0, 4], [1, 0], "k--")
    plt.xticks([0, 1, 2, 3, 4])
    ylocs, ylabels = plt.yticks()
    plt.yticks(ylocs, [])
    plt.xlabel("$\sigma_{in}$ (ms)")
    # plt.ylabel("$\overline{M}$")
    plt.subplots_adjust(bottom=0.15, top=0.95, left=0.2, right=0.95)
    filename = "figures/SigmM_{}_{}_{}".format(Nin, weight, fout).replace(".", "")
    plt.savefig(filename+".pdf")
    plt.savefig(filename+".png")
    print("{} saved".format(filename))
    plt.figure("NPSS", figsize=(4,3))
    for interpol in interpolations:
        plt.clf()
        plt.imshow(mnpss, aspect="auto", origin="lower", extent=imextent,
                   interpolation=interpol, vmin=0, vmax=1)
        cbar = plt.colorbar()
        cbar.set_label("$\overline{M}$")
        cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
        plt.xticks([0, 0.5, 1.0])
        plt.yticks([0, 1.0, 2.0, 3.0, 4.0])
        plt.xlabel("$S_{in}$")
        plt.ylabel("$\sigma_{in}$ (ms)")
        filename = "figures/npss_{}_{}_{}_{}".format(Nin, weight, fout,
                                                     interpol).replace(".", "")

        plt.subplots_adjust(bottom=0.25, top=0.95, left=0.2, right=0.8)
        plt.savefig(filename+".pdf")
        plt.savefig(filename+".png")
        print("{} saved".format(filename))
