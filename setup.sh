#!/bin/bash
#SBATCH --account=def-amoon
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=1G

#sudo add-apt-repository ppa:deadsnakes/ppa 
#sudo apt-get update 
#sudo apt-get install python3.6 python3.6-dev python3.6-venv
#python3.6 -m venv venv_prac #doesn't work

#module load python/3.6

virtualenv --python=/usr/bin/python3.6 venv
source venv/bin/activate

pip install -r ~/Documents/2022-meng/chen/Python-RVO2/requirements.txt
cd ~/Documents/2022-meng/chen/Python-RVO2/
python ~/Documents/2022-meng/chen/Python-RVO2/setup.py build
python ~/Documents/2022-meng/chen/Python-RVO2/setup.py install


cd ~/Documents/2022-meng/chen/CrowdNav/
echo '3'
yes | pip install -e ~/Documents/2022-meng/chen/CrowdNav/.

cd ~/Documents/2022-meng/chen/CrowdNav/crowd_nav/
echo '4'
yes Y | python ~/Documents/2022-meng/chen/CrowdNav/crowd_nav/train.py --policy sarl
