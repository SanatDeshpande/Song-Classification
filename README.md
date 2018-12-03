#
Song-Classification

To Setup Environment (run in sequence)

wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-MacOSX-x86_64.sh

bash Anaconda3-5.3.0-MacOSX-x86_64.sh

#say yes/agree, etc, to install. No need to install VS Code if prompted

conda update conda

conda create -n DL jupyter python=3.6 pytorch=0.4.1 torchvision=0.2.1 matplotlib=2.2.3 nltk=3.3.0 -c pytorch

To activate virtual environment:
source activate DL

To deactivate:
source deactivate


To Prepare Data:

#download data
wget http://opihi.cs.uvic.ca/sound/genres.tar.gz

#extract file
tar xzf genres.tar.gz

Here, we do a weird data transform that I don't quite understand yet. It's called a mel-spectrogram.
First, pip install librosa.

y, sr = librosa.load(filename) #will load your file.
transformed = librosa.features.melspectrogram(y=y, sr=sr, n_mels=64, hop_length=256)

#transformed is what we want, and it's supposedely a useful way of handling the sound data, but I'm not too sure yet what this buys us