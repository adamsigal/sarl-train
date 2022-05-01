#!/bin/bash

# sudo add-apt-repository ppa:deadsnakes/ppa
# sudo apt-get update
# sudo apt-get install python3.6 python3.6-dev python3.6-venv
#python3.6 -m venv venv_prac #doesn't work

#module load python/3.6

virtualenv --python=/usr/bin/python3.6 venv
source venv/bin/activate

cd ~/Documents/2022-meng/sarl-train/Python-RVO2/
pip install -r ~/Documents/2022-meng/sarl-train/Python-RVO2/requirements.txt
python ~/Documents/2022-meng/sarl-train/Python-RVO2/setup.py build
python ~/Documents/2022-meng/sarl-train/Python-RVO2/setup.py install


cd ~/Documents/2022-meng/sarl-train/CrowdNav/
#echo '3'
yes | pip install -e ~/Documents/2022-meng/sarl-train/CrowdNav/.

cd ~/Documents/2022-meng/sarl-train/CrowdNav/crowd_nav/
#echo '4'
#yes Y | python ~/Documents/2022-meng/sarl-train/CrowdNav/crowd_nav/train.py --policy sarl
