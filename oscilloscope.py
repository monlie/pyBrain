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

    def sampling(self, t):
        return

    def get_sample(self):
        return zip(*self.sample)

    def display(self, **keyargs):
        fig = plt.figure(**keyargs)
        t, x = self.get_sample()
        plt.plot(t, x)
        return fig

    
class VoltageOscilloscope(Oscilloscope):

    def sampling(self, t):
        self.sample.append((t, self.target.status[0]))

    def display(self, **keyargs):
        fig = super(VoltageOscilloscope, self).display(**keyargs)
        plt.xlabel(r"$t\ [ms]$")
        plt.ylabel(r"$V\ [mV]$")
        return fig
