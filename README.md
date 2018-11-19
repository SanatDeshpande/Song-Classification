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

reduce_rate.py takes song files and reduces the frame_rate to make it more workable

prepare_data.py takes all songs and splits them into 3-second chunks, and also makes
accompanying labels.

The command line arg instructions should be visible when you try to run them.
I recommend reducing to frame rate of 5000, but we can play around with that
