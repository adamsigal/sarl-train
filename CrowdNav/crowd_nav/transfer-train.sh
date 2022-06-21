##script
#!/bin/bash
python train.py --policy cadrl --env_config configs/env_curr_multi-pt1.config --output_dir data/cadrl_curr_multi1 --train_config configs/train_curr_pt1.config

cp configs/env_curr_multi-pt2.config data/cadrl_curr_multi1/env_curr_multi-pt2.config
cp configs/train.config data/cadrl_curr_multi1/train.config

python train.py --policy cadrl --env_config configs/env_curr_multi-pt2.config --output_dir data/cadrl_curr_multi1 --train_config configs/train.config --resume


#============================


python train.py --policy lstm_rl --env_config configs/env_curr_multi-pt1.config --output_dir data/lstm_rl_curr_multi1 --train_config configs/train_curr_pt1.config

cp configs/env_curr_multi-pt2.config data/lstm_rl_curr_multi1/env_curr_multi-pt2.config
cp configs/train.config data/lstm_rl_curr_multi1/train.config

python train.py --policy lstm_rl --env_config configs/env_curr_multi-pt2.config --output_dir data/lstm_rl_curr_multi1 --train_config configs/train.config --resume


#============================
#============================


python train.py --policy cadrl --env_config configs/env_curr-pt1.config --output_dir data/cadrl_curr1 --train_config configs/train_curr_pt1.config

cp configs/env_curr-pt2.config data/cadrl_curr1/env_curr-pt2.config
cp configs/train.config data/cadrl_curr1/train.config

python train.py --policy cadrl --env_config configs/env_curr-pt2.config --output_dir data/cadrl_curr1 --train_config configs/train.config --resume


#============================


python train.py --policy lstm_rl --env_config configs/env_curr-pt1.config --output_dir data/lstm_rl_curr1 --train_config configs/train_curr_pt1.config

cp configs/env_curr-pt2.config data/lstm_rl_curr1/env_curr-pt2.config
cp configs/train.config data/lstm_rl_curr1/train.config

python train.py --policy lstm_rl --env_config configs/env_curr-pt2.config --output_dir data/lstm_rl_curr1 --train_config configs/train.config --resume


#============================

python train.py --policy lstm_rl --env_config configs/env_multi-test_bl-cr.config --output_dir data/lstm_rl_div1 --train_config configs/train.config




