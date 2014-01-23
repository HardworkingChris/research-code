from brian import *
import neurotools as nt

dura = 0.1*second
r = 100*Hz
s = 1
j = 10*ms
n = 20

generator = nt.SynchronousInputGroup(n,r,s,j)
inp_gens = generator()
inp = MultipleSpikeGeneratorGroup(inp_gens)

inp_mon = SpikeMonitor(inp)
run(dura, report='stdout')

