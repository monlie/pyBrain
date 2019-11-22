import numpy as np 
from Synapses import synapse
from random import random


class SpikingNN(object):

    def __init__(self):
        super().__init__()

    def build(self):
        pass


class Encoder(object):

    def __init__(self, p=0.08):
        self.prob = p
        self.postsynapses = []

    def link_with(self, post_neuron):
        syn = synapse.ChemicalSynapse(self, 0.4, 0.4)
        self.postsynapses.append(syn)
        post_neuron.presynapses.append(syn)

    def fire(self, t):
        for syn in self.postsynapses:
            syn.simulate(t)

    def is_over_threshold(self, dt):
        return random() <= dt * self.prob