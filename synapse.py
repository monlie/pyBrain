import numpy as np
from math import exp


"""
Observer Pattern: treat synapses as observers, and presynaptic neurons as subjects.
REMEMBER: SUBJECTS MUST BE PRE-NEURONS!
"""
class ChemicalSynapse(object):

    # formulas could be seen on: https://www.ncbi.nlm.nih.gov/pubmed/15142958
    def __init__(self, preneuron, ampa, nmda):
        self.preneuron = preneuron
        self.g_ampa = ampa
        self.g_nmda = nmda
        self.final_spike_time = -100.0

    """
    Receptors could be further abstracted as classes, but at the same time 
    it takes much performance damage because Python interpreter cannot make 
    loop unwinding automatically, which leads me to hard code them on the current term. 
    """
    def get_current(self, t, v):
        t = t - self.final_spike_time
        g_ampa = self.g_ampa * exp(-t * 0.2)    # g' = -g / 5
        g_nmda = self.g_nmda * exp(-t * 0.006667)  # g' = -g / 150
        current = g_ampa * v        # g_ampa (v - 0)
        tmp = (v + 80) / 60
        tmp *= tmp
        current += g_nmda * v * tmp / (1 + tmp)
        return current

    def simulate(self, t):
        self.final_spike_time = t