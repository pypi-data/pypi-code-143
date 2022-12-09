"""
========
Gaussian
========
:class:`~sinabs.activation.Gaussian` surrogate gradient.
"""

import matplotlib.pyplot as plt
import torch

import sinabs.activation as sina

x = torch.linspace(-2, 4, 500)
plt.plot(x, sina.Gaussian()(v_mem=x, spike_threshold=1.0), label="Gaussian")
plt.xlabel("Neuron membrane potential")
plt.ylabel("Derivative")
plt.legend()
plt.show()
