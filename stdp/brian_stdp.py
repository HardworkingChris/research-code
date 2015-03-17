from brian import *

Ninputs = 250
eqs = "dV/dt = (Vrest-V)/tau : volt"
Vrest = -65*mV
Vth = -50*mV
tau = 10*ms
trefr = 2*ms

weight_limit = 1.0*mV

neuron = NeuronGroup(1, eqs, threshold="V>=Vth", refractory=trefr, reset=Vrest)
neuron.V = Vrest

poisson_inputs = PoissonGroup(Ninputs, rates=10*Hz)
connections = Connection(poisson_inputs, neuron, state="V")
connections[:,0] = rand(Ninputs)*weight_limit

tau_pre  = 10*ms
tau_post = 10*ms
dA_pre  =  0.0005
dA_post = -0.0005
stdp_eqs = """
dA_pre/dt  = -A_pre/tau_pre   : 1
dA_post/dt = -A_post/tau_post : 1
"""
stdp = STDP(connections, stdp_eqs,
            pre="A_pre+=dA_pre; w+=A_post",
            post="A_post+=dA_post; w+=A_pre",
            wmax=weight_limit,
            wmin=-weight_limit*0.5)

voltmon = StateMonitor(neuron, "V", record=True)
spikemon = SpikeMonitor(neuron)

#decaclock = Clock(dt=10*ms)
weightmon = []
nsp = 0

@network_operation
def record_weights(clock):
    if clock.t in spikemon.spiketimes[0]:
        weightmon.append(connections[:,0].todense())

run(5*second, report="stdout")

voltmon.insert_spikes(spikemon, 10*mV)

weightmon = array(weightmon)
figure("voltage")
plot(voltmon.times, voltmon[0])
figure("weight histogram")
hist(connections[:,0])
figure("weights across time")
mweight = mean(weightmon, axis=1)
sweight = std(weightmon, axis=1)
plot(spikemon.spiketimes[0], mweight)
plot(spikemon.spiketimes[0], mweight+sweight, "r--")
plot(spikemon.spiketimes[0], mweight-sweight, "r--")
show()
