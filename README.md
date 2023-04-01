# HRI (NAO environment)

All the projects related to NAO in the dev env, made by sougato is kept here. Feel free to peek into our code and refer. 

## My setup 
- I am using windows 11 (WSL - Ubuntu 18)
- For gpu setup please install, nvidia cuda toolkit on windows 
- Your distro will be able to access the gpu drivers. 
- You need to install USBIPD on windows 
- Follow the steps from this website :
  - https://learn.microsoft.com/en-us/windows/wsl/connect-usb
- The audio drivers might not be present by default, need to install PulseAudio 

## Installation
To install this project, follow these steps:
- Install Miniconda (https://docs.conda.io/en/latest/miniconda.html)
- Go to https://www.aldebaran.com/en/support/nao-6/downloads-softwares
- In your home dir create a folder "naoqi" and then download the python SDK there and extract.
  - add "export PYTHONPATH=~/naoqi/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327/lib/python2.7/site-packages:$PYTHONPATH" to your .bashrc

Install PulseAudio, pavucontrol is for GUI
```bash
sudo apt update
sudo apt install pulseaudio -y
sudo apt install pavucontrol -y
```  
Create Conda env
```bash
conda create --name hri
conda activate hri
```
Install PyTorch GPU
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```
Install record audio libraries
```bash
conda install -c anaconda pyaudio
```
Install Voice Authentication module
```bash
pip install pyannote.audio
```
Install OpenAI for chatGPT integration 
```bash
conda install -c conda-forge openai
```
Install Whisper voice trascription model 
```bash
pip install -U openai-whisper
pip install git+https://github.com/openai/whisper.git 
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
sudo apt update && sudo apt install ffmpeg

```
This code needs API keys from OPENAI(for chatGPT) and huggingface.co(for pyannote)
- I have added these keys to the .bashrc file 
- OpenAI link - https://platform.openai.com/account/api-keys
```bash
export OPENAI_API_KEY="you-key-please"
```
- HuggingFace link - https://huggingface.co/settings/tokens
- Also you have to agree to some T&C. Preferably run it 1st time on jupyter, you will get the link there itself.
```bash
export PYANNOTE_API_KEY="you-key-please"
```


You may need to create an ssh setup for GitHub
- Follow the comands below, you may discard the prompts 
- copy and paste the id_rsa.pub contents to https://github.com/settings/keys
```bash
ssh-keygen -t rsa -b 4096 -C "email@domain.com"
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
git config --global user.email "email@domain.com"
git config --global user.name "Jon Doe"
```
