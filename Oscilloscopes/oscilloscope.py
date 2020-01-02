import numpy as np
import matplotlib.pyplot as plt


class Recordable(object):

    def __init__(self):
        self.oscilloscopes = []
    
    def attach(self, osc):
        self.oscilloscopes.append(osc)

    def record_to_oscilloscopes(self, t):
        for osc in self.oscilloscopes:
            osc.sampling(t)


# Observer Pattern: treat oscilloscopes as observers
class Oscilloscope(object):

    def __init__(self, target):
        self.target = target
        self.sample = []
        target.attach(self)

    def reboot(self):
        self.sample = []

    def sampling(self, t):
        return

    def get_sample(self):
        return list(zip(*self.sample))

    def display(self, ax, **keyargs):
        sample = self.get_sample()
        if sample:
            t, x = sample
            ax.plot(t, x, **keyargs)
        return ax

    
class VoltageOscilloscope(Oscilloscope):

    def sampling(self, t):
        self.sample.append((t, self.target.status[0]))

    # # override
    # def display(self, fig, **keyargs):
    #     fig = super(VoltageOscilloscope, self).display(fig, **keyargs)
    #     plt.xlabel(r"$t\ [ms]$")
    #     plt.ylabel(r"$V\ [mV]$")
    #     return fig


class SpikingOscilloscope(Oscilloscope):

    def sampling(self, t):
        self.sample.append((t, 30))
    
    # override
    def display(self, ax, **keyargs):
        sample = self.get_sample()
        if sample:
            t, x = sample
            ax.scatter(t, x, **keyargs)
            # plt.xlabel(r"$t\ [ms]$")
            # plt.ylabel(r"$V\ [mV]$")
        return ax
