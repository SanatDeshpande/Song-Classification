import matplotlib.pyplot as plt

import itertools
import sys

# import IPython.display as ipd
import numpy as np

with open(sys.argv[1], "r") as f:
    training = [float(i) for i in f.read().split(",")[:-1]]
with open(sys.argv[2], "r") as f:
    validation = [float(i) for i in f.read().split(",")[:-1]]
plt.figure()
plt.plot(np.arange(len(training)), training, np.arange(len(validation)), validation)
plt.legend(['Train acc', 'Val acc'])
plt.show()