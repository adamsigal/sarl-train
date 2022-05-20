# Improving Reinforcement Learning Training Regimes for Social Robot Navigation

The code in this repository is based on **Crowd-Robot Interaction: Crowd-aware Robot Navigation with Attention-based Deep Reinforcement Learning** [[Paper](https://arxiv.org/abs/1809.08835)], [[GitHub](https://github.com/vita-epfl/CrowdNav)]. This repository contains all of the code of Python-RVO2 (`sarl-train/Python-RVO2/`) [[GitHub](https://github.com/sybrenstuvel/Python-RVO2)], the official implementation of ORCA [[Paper](https://gamma.cs.unc.edu/ORCA/publications/ORCA.pdf)], used in Chen et al.'s original work. This repository also contains code based on Deep Social Force (`sarl-train/CrowdNav/crowd_sim/envs/policy/socialforce/`) [[Paper](https://arxiv.org/abs/2109.12081)], [[GitHub](https://github.com/svenkreiss/socialforce)] (version 0.1.0).
<!-- It would have been a fork from their repository, but technical difficulties caused me to create a separate one containing mainly their code, but also others.  -->

<!-- I know that you instructed us to not copy entire repositories of code, but RVO2 gave me a lot of trouble in installation, so having the whole thing in this repository will greatly simplify things. I discussed this with you in class and you said it was acceptable.  -->


## Abstract
Autonomous mobile robots are increasingly expanding into human spaces. In order for this process to continue smoothly and successfully, many factors, both social and technological must be carefully considered. One critical example is the problem of navigation while abiding by social norms in pedestrian spaces, often known simply as the social navigation problem. Recently, there have been approaches that use reinforcement learning (RL) to train policies that can approach this task more efficiently than earlier methods. In one prominent example, Chen et al. [[1](https://arxiv.org/abs/1809.08835)] proposed to address this by taking into consideration not only pairwise human-robot interaction, but also the cumulative effect of the crowd as a whole. However, as with most RL social navigation research, Chen et al. train their algorithm on data generated by only one behavioural model: ORCA [[2](https://gamma.cs.unc.edu/ORCA/publications/ORCA.pdf)]. This study proposes to address the problem of homogeneous training environments by also including pedestrians modelled by Social Force [[3](https://arxiv.org/abs/cond-mat/9805244)] in training and testing. Through evaluation in larger and more crowded environments, the results suggest that beginning training in a simpler homogeneous setting, and then transferring to a more diverse one halfway through stimulates significant gains in generalization performance.

### Files Changed

Modifications and additions were made to almost every file and folder in `CrowdNav/crowd_nav/`. Major modifications were made to `CrowdNav/crowd_sim/crowd_sim.py`, and minor modifications were made to files in `CrowdNav/crowd_sim/utils/`. Succinct, but crucial modifications were made in `CrowdNav/crowd_sim/policy/` and especialy in `CrowdNav/crowd_sim/policy/socialforce/`.

## Method Overview (Figure from [[Chen et al.](https://github.com/vita-epfl/CrowdNav)])
<img src="https://i.imgur.com/YOPHXD1.png" width="1000" />

## Setup
The code in this repository is based on Python 3.6. It is recommended to create a virtualenv. The following steps were tested in Ubuntu 20.04.

1. Download python 3.6 and the corresponding `pip` and `virtualenv` releases if your distribution does not have them already.
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev python3.6-venv
sudo python3.6 -m pip install virtualenv
```

2. Navigate to the repository and activate venv.
```
cd /path/to/sarl-train/
virtualenv --python=/usr/bin/python3.6 venv
source venv/bin/activate
```

3. Install RVO2 (ORCA). If you run into problems, refer to the [repo](https://github.com/sybrenstuvel/Python-RVO2).
```
cd Python-RVO2/
pip install -r requirements.txt
python setup.py build
python setup.py install
```

4. Install CrowdNav.
```
cd .. # navigate back to main sarl-train directory
pip install -r requirements.txt
cd CrowdNav
yes | pip install -e .
```

This should work, but it is possible for issues to arise. If you are unable get it working, please email me.


## Getting Started
This repository is organized in two parts: CrowdNav/crowd_sim/ folder contains the simulation environment and
CrowdNav/crowd_nav/ folder contains codes for training and testing the policies. Details of the simulation framework can be found [here](CrowdNav/crowd_sim/README.md). Below are the instructions for training and testing policies, and they should be executed inside the crowd_nav/ folder. Note that in this repo 3 pretrained models are included: LM-SARL, Multi-SARL, and Transfer-SARL

From the **main `sarl-train` directory**, navigate to the crowd_nav folder.
```
cd CrowdNav/crowd_nav/
```

Optional: Train a policy in a diverse environment (will take 10+ hours).
```
python train.py --policy sarl --env_config configs/env_multi-test_bl-cr.config
```

Test policies over 50 test episodes with pretrained models.
```
python test.py --policy orca --phase test --env_config configs/env_multi-test_bl-sq.config
python test.py --policy sarl --model_dir data/output_transfer_sarl --phase test --env_config configs/env_multi-test_dn-sq.config
```
Run a pretrained model for one episode and visualize the result.
```
python test.py --policy sarl --model_dir data/output_lm_sarl --phase test --env_config configs/env_multi-test_lg-cr.config --visualize --test_case 0
python test.py --policy sarl --model_dir data/output_multi_sarl --phase test --env_config configs/env_multi-test_lg-sq.config --visualize --test_case 0
```
Plot the training curves of the pretrained models: LM-SARL, Multi-SARL, and Transfer-SARL.
```
python utils/plot.py data/output_lm_sarl/output.log data/output_multi_sarl/output.log data/output_transfer_sarl/output.log
```


## Simulation Videos (Multi-SARL)
Baseline Circle Crossing             | Baseline Square Crossing
:-------------------------:|:-------------------------:
<img src="https://i.imgur.com/8Ru0I1u.gif" width="400" />|<img src="https://i.imgur.com/zwRfDBB.gif" width="400" />
**Large Circle Crossing**             | **Large Square Crossing**
<img src="https://i.imgur.com/Rh88H52.gif" width="400" />|<img src="https://i.imgur.com/ensprho.gif" width="400" />
**Dense Circle Crossing**             | **Dense Square Crossing**
<img src="https://i.imgur.com/SfKSlXZ.gif" width="400" />|<img src="https://i.imgur.com/D4453gj.gif" width="400" />  |  

## Collision Case in Dense Square Crossing
LM-SARL (Collision)             | Transfer-SARL (Avoids Collision)
:-------------------------:|:-------------------------:
<img src="https://i.imgur.com/4AvnPd1.gif" width="400" />|<img src="https://i.imgur.com/d7l7rNI.gif" width="400" />

## Learning Curve
Learning curve comparison between different methods.

<img src="https://i.imgur.com/SInXYTC.png" width="600" />
