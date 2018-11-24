import numpy as np
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__():
        self.conv1 = nn.Conv2d(1, 64, kernel_size=(3,3))
        self.conv2 = nn.Conv2d(64, 64, kernel_size=(3,5))
        self.fc1 = nn.Linear(12544, 32)
        self.fc2 = nn.Linear(32, 10)
        self.dropout = nn.Dropout(.2)
    def forward(self, x):
        x = x.view(-1, 1, 64, 256)
        x = F.relu(self.conv1(x))
        x = self.dropout(x)
        x = F.max_pool2d(x, (2,4))
        x = F.relu(self.conv2(x))
        x = self.dropout(x)
        x = F.max_pool2d(x, (2,4))
        x = x.view(-1, 12544)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return F.softmax(x, dim=1)

def assess(model, songs, labels):
    model.eval()
    correct = 0
    total = 0
    for i in range(50):
        index = np.random.randint(len(labels))
        pred = model(songs[index])
        if torch.argmax(pred, dim=1) == labels[index]:
            correct += 1
        total += 1
    model.train()
    return correct/total

with np.load("../audio_sr_label.npz") as f:
    data = f['X']
    labels = list(f['T'])
data = np.asarray([[i[:2560] for i in j] for j in data])
seed = data[:, :, :256]
for i in range(1, 10):
    seed = np.append(seed, data[:, :, i*256:(i+1)*256], axis=0)
data = torch.tensor(seed, dtype=torch.float)
labels = labels * 10 #expand dimensions accordingly
label_set = set(labels)
mapping = {}
for count, i in enumerate(label_set):
    mapping[i] = count
targets = np.zeros(len(labels))
for i in range(len(targets)):
    targets[i] = mapping[labels[i]]
targets = torch.tensor(targets, dtype=torch.long)

labels_train = targets[int(len(targets)/10):]
labels_test = targets[:int(len(targets)/10)]
data_train = data[int(len(data)/10):]
data_test = data[:int(len(data)/10)]
#double check ^^ above stuff


model = Model()
optimizer = optim.Adam(list(model.parameters()), lr=1e-5)
if torch.cuda.is_available():
    model.cuda()
    data_train.cuda()
    data_test.cuda()
    labels_train.cuda()
    labels_test.cuda()

training_acc = []
validation_acc = []
model.train()
for epoch in range(1):
    for i in range(len(labels_train)):
        index = np.random.randint(len(labels_train))
        optimizer.zero_grad()
        target = labels_train[index]
        prediction = model(data_train[index])
        criterion = nn.CrossEntropyLoss()
        loss = criterion(prediction, target.unsqueeze(0))
        loss.backward()
        optimizer.step()
        if i % 5 == 0:
            print("loss: ", loss)
            if i % 20 == 0:
                training_acc.append(assess(model, data_train, labels_train))
                validation_acc.append(assess(model, data_test, labels_test))
                print(training_acc[-1], validation_acc[-1])
