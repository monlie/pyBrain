import numpy as np
import matplotlib.pyplot as plt


# Observer Pattern: treat oscilloscopes as observers
class Oscilloscope(object):

    def __init__(self, neuron):
        self.target = neuron
        self.sample = []
        neuron.attach(self)

    def reboot(self):
        self.sample = []

    def sampling(self, t, dt):
        return

    def get_sample(self):
        return zip(*self.sample)

    def display(self, fig, as_scatter=False, **keyargs):
        t, x = self.get_sample()
        if as_scatter:
            plt.scatter(t, x, **keyargs)
        else:
            plt.plot(t, x, **keyargs)
        return fig

    
class VoltageOscilloscope(Oscilloscope):

    def sampling(self, t, dt):
        self.sample.append((t, self.target.status[0]))

    def display(self, fig, as_scatter=False, **keyargs):
        fig = super(VoltageOscilloscope, self).display(fig, as_scatter, **keyargs)
        plt.xlabel(r"$t\ [ms]$")
        plt.ylabel(r"$V\ [mV]$")
        return fig


class PreSpikingOscilloscope(VoltageOscilloscope):

    def sampling(self, t, dt):
        if self.target.has_prespiking:
            self.sample.append((t - dt, 30))
    
    def display(self, fig, **keyargs):
        fig = super(PreSpikingOscilloscope, self).display(fig, True, **keyargs)
        return fig