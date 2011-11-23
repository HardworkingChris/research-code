from brian import *
import brian_no_units	
from time import time
from numpy import *
from scipy import *

#ERROR

eqs=Equations('''
dv/dt = (-gL*(v-VL)-gK*n*n*n*n*(v-VK)-gNa*h*m*m*m*(v-VNa)+J1)/Cm : 1
dm/dt = (minfty-m)/(taum)  : 1
dn/dt = (ninfty-n)/(taun)  : 1
dh/dt = (hinfty-h)/(tauh)  : 1
alpham = 0.1*(v+40)/(1-exp(-0.1*(v+40)))  : 1
alphah = 0.07*exp(-0.05*(v+65))  : 1
alphan = 0.01*(v+55)/(1-exp(-0.1*(v+55)))  : 1
betam = 4.0*exp(-0.0556*(v+65)) : 1
betah = 1.0/(1+exp(-0.1*(v+35)))  : 1
betan = 0.125*exp(-0.0125*(v+65))  : 1
taum = 1.0/(alpham+betam)  : 1
taun = 1.0/(alphan+betan)  : 1
tauh = 1.0/(alphah+betah)  : 1
minfty = alpham*taum  : 1
ninfty = alphan*taun  : 1
hinfty = alphah*tauh  : 1
Cm = 1  : 1
gL = 0.3 : 1
gK = 36  : 1
gNa = 120  : 1
VL = -54.402 : 1
VK = -77  : 1
VNa = 50  : 1
J1=10 : 1
''')


P = NeuronGroup(1, model=eqs, method='RK', freeze=True)


#M = SpikeMonitor(neuron1)
#rate = PopulationRateMonitor(neuron1)

#trace = StateMonitor(neuron1, 'v', record=True)
#start_time=time()
#run(duration)
#print "Simulation time:",time()-start_time
#clf()
#figure(1)
#subplot(221)
#plot(rate.times,rate.rate)

#run(100 * ms)
#neuron.I = 10 * uA
#run(100 * ms)
#plot(trace.times / ms, trace[0] / mV)
#plot(trace.times,trace[0])
#show()

