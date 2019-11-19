import numpy as np


class Integrator(object):

    def __init__(self, neu, ts=5e-2):
        self.neurons = neu
        self.time_step = ts

    # one step iteration using 4th-order Runge-Kutta method
    @staticmethod
    def one_step_rk45(neu, x, t, dt):
        halfdt = dt * 0.5
        k1 = neu.dynamic_equ(t, x)
        k2 = neu.dynamic_equ(t + halfdt, x + halfdt * k1)
        k3 = neu.dynamic_equ(t + halfdt, x + halfdt * k2)
        k4 = neu.dynamic_equ(t + dt, x + dt * k3)
        x = x + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
        return x

    # binary search the precise time of spiking
    @classmethod
    def search_t(cls, neu, t, ldt, rdt):
        dt = (rdt + ldt) * 0.5
        x = cls.one_step_rk45(neu, neu.status, t, dt)
        if x[0] >= 30:
            return cls.search_t(neu, t, ldt, dt)
        if 30 - x[0] > 1e-6:
            return cls.search_t(neu, t, dt, rdt)
        return x, dt

    def integrate(self, steps=1000, callback=lambda _neuron, _t, _dt : None):
        t = 0.0
        dt = self.time_step

        for _ in range(steps):
            callback(self.neurons, t, dt)                   # presynaptic spiking
            dt = self.time_step
            x = self.one_step_rk45(self.neurons, self.neurons.status, t, dt)

            is_over_threshold = x[0] >= 30
            if is_over_threshold:
                x, dt = self.search_t(self.neurons, t, 0, dt)

            self.neurons.status = x
            t += dt
            self.neurons.record_to_oscilloscopes(t)     # Observer Pattern: treat oscilloscopes as observers

            if is_over_threshold:
                self.neurons.reset()
