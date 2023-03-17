# HRI (NAO environment)

All the projects related to NAO in the dev env, made by sougato is kept here. Feel free to peek into our code and refer. 

## My setup 
- I am using windows 11 (WSL - Ubuntu 18)
- For gpu setup please install, nvidia cuda toolkit on windows 
- Your distro will be able to access the gpu drivers. 

## Installation
To install this project, follow these steps:
- Install Miniconda (https://docs.conda.io/en/latest/miniconda.html)
- Go to https://www.aldebaran.com/en/support/nao-6/downloads-softwares
- In your home dir create a folder "naoqi" and then download the python SDK there and extract.
  - add "export PYTHONPATH=~/naoqi/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages:$PYTHONPATH" to your .bashrc
- Run the following commands:

```bash
# Create Conda env
conda create --name hri
conda activate hri
# Install PyTorch GPU
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
# Install Voice Authentication module
pip install pyannote.audio
# Install OpenAI for chatGPT integration 
conda install -c conda-forge openai
# Install Whisper voice trascription model 
pip install -U openai-whisper
pip install git+https://github.com/openai/whisper.git 
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
sudo apt update && sudo apt install ffmpeg

```
