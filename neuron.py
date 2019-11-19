import numpy as np
from math import exp
from random import random
import synapse


class IzhikevichNeuron(object):
    
    def __init__(self, ts=5e-2, a=0.02, b=0.2, c=-65.0, d=8.0):
        self.time_stamp = None
        self.status = np.array([-70.0, -14.0], dtype=np.float64)
        self.time_step = ts
        
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        
        self.presynapses = []
        self.postsynapses = []

        self.oscilloscopes = []

    # can be seen on: https://www.izhikevich.org/publications/spikes.htm
    def izhikevich_equs(self, t, x):
        v, u = x
        dv = 0.04 * v*v + 5 * v + 140 - u - self.total_current(t, v)
        du = self._a * (self._b * v - u)
        return np.array([dv, du], dtype=np.float64)
    
    # repolarization
    def reset(self):
        self.status[0] = self._c
        self.status[1] += self._d
        
    def total_current(self, t, v):
        return sum([syn.get_current(t, v) for syn in self.presynapses])

    # one step iteration using 4th-order Runge-Kutta method
    def one_step_rk45(self, x, t, dt):
        halfdt = dt * 0.5
        k1 = self.izhikevich_equs(t, x)
        k2 = self.izhikevich_equs(t + halfdt, x + halfdt * k1)
        k3 = self.izhikevich_equs(t + halfdt, x + halfdt * k2)
        k4 = self.izhikevich_equs(t + dt, x + dt * k3)
        x = x + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
        return x
    
    def integrate(self, steps=1000, callback=lambda _neuron, _t, _dt : None):
        t = 0.0
        dt = self.time_step

        for _ in range(steps):
            callback(self, t, dt)                   # presynaptic spiking
            dt = self.time_step
            x = self.one_step_rk45(self.status, t, dt)

            is_over_threshold = x[0] >= 30
            if is_over_threshold:
                x, dt = self.search_t(t, 0, dt)

            self.status = x
            t += dt
            self.record_to_oscilloscopes(t, dt)     # Observer Pattern: treat oscilloscopes as observers

            if is_over_threshold:
                self.reset()

    def fire(self, t):
        for syn in self.postsynapses:
            syn.simulate(t)
    
    # binary search the precise time of spiking
    def search_t(self, t, ldt, rdt):
        dt = (rdt + ldt) * 0.5
        x = self.one_step_rk45(self.status, t, dt)
        if x[0] >= 30:
            return self.search_t(t, ldt, dt)
        if 30 - x[0] > 1e-6:
            return self.search_t(t, dt, rdt)
        return x, dt

    def attach(self, osc):
        self.oscilloscopes.append(osc)

    def record_to_oscilloscopes(self, t, dt):
        for osc in self.oscilloscopes:
            osc.sampling(t, dt)

    def link_with(self, post_neuron):
        syn = synapse.ChemicalSynapse(self, 0.4, 0.4)
        self.postsynapses.append(syn)
        post_neuron.presynapses.append(syn)
