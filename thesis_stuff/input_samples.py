import spikerlib as sl
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['text.usetex']=True
mpl.rcParams['text.latex.unicode']=True

N = 50
f = 40
dura = 1
ms = 0.001

configs = [(0.2, 0*ms), (0.2, 3*ms), (0.8, 0*ms), (0.8, 3*ms)]
spikegroups = []
spikemonitors = []
plt.figure(figsize=(4,3))
for i, c in enumerate(configs):
    group = sl.tools.fast_synchronous_input_gen(N, f, c[0], c[1], dura,
                                                shuffle=True)
    spikes = group.get_spiketimes()
    plt.clf()
    for sp in spikes:
        plt.plot(sp[1], sp[0], 'b.', markersize=3)
    # plt.title(r"$S_{{in}}=~{},~\sigma_{{in}}=~{}~\mathrm{{ms}}$".format(*c))
    xticks = plt.xticks()
    yticks = plt.yticks()
    if i == 0:
        plt.xticks(xticks[0], "")
    elif i == 1:
        plt.xticks(xticks[0], "")
        plt.yticks(yticks[0], "")
    elif i == 2:
        plt.xlabel("t (s)")
    elif i == 3:
        plt.yticks(yticks[0], "")
        plt.xlabel("t (s)")
    filename = "input_sample_{}_{}".format(*c).replace(".", "")
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(filename+".pdf")
    print("Saved {}".format(filename))
