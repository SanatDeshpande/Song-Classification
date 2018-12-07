import matplotlib.pyplot as plt

import os
import itertools
import sys

# import IPython.display as ipd
import numpy as np
import pandas as pd
import torch
from torch.autograd import Variable
import torch.nn.functional as F

from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix

import datetime


# From https://github.com/mdeff/fma/blob/master/utils.py

import ast

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    cm = np.asarray(cm)
    nans = np.isnan(cm)
    cm[nans] = 0.0
    print(cm)
    

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt,),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black",
                 fontsize=6)

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

fig = plt.figure()
# fig.set_size_inches(7.0, 7.0, forward=True)

with open(sys.argv[1], "r") as f:
    label_batch = f.read().split(",")
with open(sys.argv[2], "r") as f:
    pred_batch = f.read().split(",")
# classes = sorted(list(set(pred_batch)))
classes = ['disco', 'jazz', 'classical', 'country', 'hiphop', 'metal', 'rock', 'pop', 'blues', 'reggae']
# cm = confusion_matrix(label_batch, pred_batch, labels=classes)
cm = confusion_matrix(label_batch, pred_batch)
print(cm)
plot_confusion_matrix(cm, classes, normalize=True, title="LSTM Confusion Matrix")
plt.show()