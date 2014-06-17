from brian import *
from spikerlib.tools import SynchronousInputGroup

dura = 0.5*second
r = 100*Hz
s = 1
j = 1*ms
n = 20

print("Constructing spike generator ...")
inp_gen = SynchronousInputGroup(n,r,s,j)
print("Setting up SpikeGeneratorGroup ...")
inp = SpikeGeneratorGroup(n, inp_gen())

inp_mon = SpikeMonitor(inp)
run(dura, report='stdout')

