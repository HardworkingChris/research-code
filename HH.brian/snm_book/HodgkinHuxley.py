from brian import *
import time

# Parameters
#area=20000*umetre**2
area = 1
Cm=(1*ufarad*cm**-2)*area
ENa=115*mV
g_na=(120*msiemens*cm**-2)*area
EK=-12*mV
g_kd=(36*msiemens*cm**-2)*area
El=10.6*mV
gl=(0.3*msiemens*cm**-2)*area
start_time=time.time()
# The model
eqs=Equations('''
dv/dt = I/farad-(gl*(v-El)+g_na*(m*m*m)*h*(v-ENa)+g_kd*(n*n*n*n)*(v-EK))/Cm : volt
dm/dt = alpham*(1-m)-betam*m : 1
dn/dt = alphan*(1-n)-betan*n : 1
dh/dt = alphah*(1-h)-betah*h : 1

alphan = (0.1-0.01*(v/mV))/(exp(1-0.1*(v/mV))-1)/ms : Hz
alpham = (2.5-0.1*(v/mV))/(exp(2.5-0.1*(v/mV))-1)/ms : Hz
alphah = 0.07*(exp(-(v/mV)/20))/ms : Hz

betan = 0.125*exp(-(v/mV)/80)/ms : Hz
betam = (4.*exp(-(v/mV)/18))/ms : Hz
betah = (1./(exp(3.-0.1*(v/mV))+1))/ms : Hz
I:amp
''')

P=NeuronGroup(1,model=eqs,\
              threshold=EmpiricalThreshold(threshold=20*mV,refractory=3*ms),\
              implicit=True,freeze=True,compile=False)

trace=StateMonitor(P,'v',record=True)
mrec = StateMonitor(P,'m',record=True)
nrec = StateMonitor(P,'n',record=True)
hrec = StateMonitor(P,'h',record=True)
spikemon=SpikeMonitor(P)

P.v = 10.6*mV

print "Simulation running..."
start_time=time.time()
P.I = 0*amp
run(100*msecond)
P.I = 10*amp
run(1*msecond)
P.I = 0*amp
run(2*second)
#P.I = 9*amp
#run(100*msecond)
#P.I = 12*amp
#run(100*msecond)
duration=time.time()-start_time
print "Simulation time:",duration,"seconds"

if (spikemon.nspikes > 0):
    isi = diff(spikemon.spiketimes[0])
    peakrate = 1./(min(isi)*second)
    print "Firing occured at:",spikemon.spiketimes
    print spikemon.nspikes,"total."
    print "Peak rate:",peakrate

subplot(2,1,1)
plot(trace.times/ms,trace[0]/mV)
subplot(2,1,2)
plot(mrec.times/ms,mrec[0],'y',nrec.times/ms,nrec[0],'b',hrec.times/ms,hrec[0],'g')
show()

print "Last voltage value:",trace[0][-1]

