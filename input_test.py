from brian import *
from spikerlib.tools import fast_synchronous_input_gen

dura = 0.5*second
r = 100*Hz
s = 0.7
j = 0.5*ms
j = 0
n = 20

#print("Constructing spike generator ...")
#inp_gen = SynchronousInputGroup(n,r,s,j)
#print("Setting up SpikeGeneratorGroup ...")
#inp = SpikeGeneratorGroup(n, inp_gen())

inp = fast_synchronous_input_gen(n, r, s, j, dura)

inp_mon = SpikeMonitor(inp)
network = Network(inp, inp_mon)
network.run(dura, report='stdout')

