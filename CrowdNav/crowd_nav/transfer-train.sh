##script
#!/bin/bash
python train.py --policy cadrl --env_config configs/env_trans-pt1.config --output_dir data/cadrl_trans1 --train_config configs/train_trans_pt1.config

cp configs/env_trans-pt2.config data/cadrl_trans1/env_trans-pt2.config
cp configs/train.config data/cadrl_trans1/train.config

python train.py --policy cadrl --env_config configs/env_trans-pt2.config --output_dir data/cadrl_trans1 --train_config configs/train.config --resume

