import spikerlib as sl
import matplotlib.pyplot as plt


N = 50
f = 20
dura = 1
ms = 0.001

configs = [(0.2, 0*ms), (0.2, 3*ms), (0.8, 0*ms), (0.8, 3*ms)]
spikegroups = []
spikemonitors = []
plt.figure()
for c in configs:
    group = sl.tools.fast_synchronous_input_gen(N, f, c[0], c[1], dura,
                                                shuffle=True)
    spikes = group.get_spiketimes()
    plt.clf()
    for sp in spikes:
        plt.plot(sp[1], sp[0], 'b.')
    filename = "input_sample_{}{}.pdf".format(*c)
    plt.savefig(filename)
    print("Saved {}".format(filename))
