# HRI (NAO environment)

All the projects related to NAO in the dev env, made by sougato is kept here. Feel free to peek into our code and refer. 


## Installation
To install this project, follow these steps:
- Install Miniconda (https://docs.conda.io/en/latest/miniconda.html)
- 
- Run the following commands:
```sh
conda create --name hri

conda activate hri

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

pip install pyannote.audio

conda install -c conda-forge openai

pip install -U openai-whisper

pip install git+https://github.com/openai/whisper.git 

pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

sudo apt update && sudo apt install ffmpeg
