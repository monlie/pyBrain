# pyBrain

A multi-model-supporting framework implemented in Python for SNN simulating. 

![](https://github.com/monlie/pyBrain/blob/master/demo/v_i.png?raw=true)

## Background

A brief introduction to SNN can be seen here: [INTRODUCTION (Chinese version)](https://)

## Supported/Supporting Features

### Neuron Models

- [x] Izhikevich neuron
- [ ] H-H neuron: low performance so perhaps it would be implemented after a long time XD)
- [ ] LIF neuron: fast but low biological plausibility

### Synapses / Receptors

- [x] AMPA receptor
- [x] NMDA receptor
- [ ] GABA_A receptor
- [ ] GABA_B receptor
- [x] electrical synapse

### Simulation Methods

- [x] clock-driven method with high precision spiking time searching
- [ ] voltage-driven: the best method so far
- [ ] event-driven (spiking-driven): best performance but cannot be generally used

### Training Algorithms

- [ ] unsupervised STDP
- [ ] supervised STDP (ReSuMe)

### Spike Coding

I am still studying it.

### Others

- [ ] oscilloscopes
- [ ] GPU acceleration