import numpy as np
from Synapses import synapse
from Oscilloscopes import Recordable

# TODO: 脉冲事件队列应该由突触前神经元维护，而非像当前版本一样由突触维护！
class Neuron(Recordable):

    def __init__(self, status=None, stimulation=None):
        super(Neuron, self).__init__()

        self.status = status
        self.stimulation = stimulation
        self.time_stamp = None 
        self.presynapses = []
        self.postsynapses = []

    # dynamic equations: dx/dt = f(t, x), wherein x is status of the neuron
    def dynamic_equ(self, t, x):
        raise NotImplementedError

    def is_over_threshold(self, v):
        return False
    
    def reset(self):
        return
        
    def total_current(self, t, v):
        current = sum([syn.get_current(t, v) for syn in self.presynapses])
        if self.stimulation is not None:
            current += self.stimulation(t)
        return current

    def fire(self, t):
        for syn in self.postsynapses:
            syn.simulate(t)

    def link_with(self, post_neuron):
        syn = synapse.ChemicalSynapse(self, 0.4, 0.4)
        self.postsynapses.append(syn)
        post_neuron.presynapses.append(syn)

    def update_synapses(self, t):
        for syn in self.presynapses:
            syn.time_manager.update(t)


class IzhikevichNeuron(Neuron):
    
    def __init__(self, status=None, stimulation=None, a=0.02, b=0.2, c=-65.0, d=8.0):
        if status is None:
            status = np.array([-70.0, -14.0], dtype=np.float64)
        super(IzhikevichNeuron, self).__init__(status, stimulation)

        self._a = a
        self._b = b
        self._c = c
        self._d = d

    # can be seen on: https://www.izhikevich.org/publications/spikes.htm
    def dynamic_equ(self, t, x):
        v, u = x
        dv = 0.04 * v*v + 5 * v + 140 - u - self.total_current(t, v)
        du = self._a * (self._b * v - u)
        return np.array([dv, du], dtype=np.float64)
    
    # repolarization
    def reset(self):
        self.status[0] = self._c
        self.status[1] += self._d

    def is_over_threshold(self, v):
        return v >= 30


# TODO: just used for test the integrator
class _TestNeuron(Neuron):
    
    def __init__(self, status=None):
        if status is None:
            status = np.array([0, 0], dtype=np.float64)
        super(_TestNeuron, self).__init__(status)

    # dx / dt = x, the solution should be x(t) = c * exp(t)
    def dynamic_equ(self, t, x):
        v, u = x
        return np.array([v, 0], dtype=np.float64)


# Factory Pattern
class NeuronFactory(object):

    _neurons = {"RS": {}, 
                "IB": {"c": -55.0, "d": 4.0},
                "CH": {"c": -50.0, "d": 2.0}}

    def __new__(cls, ntype, stim=None):
        paras = cls._neurons.get(ntype)
        if ntype is not None:
            return IzhikevichNeuron(stimulation=stim, **paras)
