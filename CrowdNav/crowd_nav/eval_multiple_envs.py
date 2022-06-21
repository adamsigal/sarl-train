import os

def eval_envs(policy, model_dir, gpu=False):
    """
    python test.py --policy sarl --phase test --model_dir data/output_sarl_bl1 --env_config configs/env_multi-test_bl-cr.config 2>&1 | tee data/output_sarl_bl1/eval/multi-bl-cr
    python test.py --policy sarl --phase test --model_dir data/output_sarl_bl1 --env_config configs/env_multi-test_bl-sq.config 2>&1 | tee data/output_sarl_bl1/eval/multi-bl-sq

    python test.py --policy sarl --phase test --model_dir data/output_sarl_bl1 --env_config configs/env_multi-test_dn-cr.config 2>&1 | tee data/output_sarl_bl1/eval/multi-dn-cr
    python test.py --policy sarl --phase test --model_dir data/output_sarl_bl1 --env_config configs/env_multi-test_dn-sq.config 2>&1 | tee data/output_sarl_bl1/eval/multi-dn-sq

    python test.py --policy sarl --phase test --model_dir data/output_sarl_bl1 --env_config configs/env_multi-test_lg-cr.config 2>&1 | tee data/output_sarl_bl1/eval/multi-lg-cr
    python test.py --policy sarl --phase test --model_dir data/output_sarl_bl1 --env_config configs/env_multi-test_lg-sq.config 2>&1 | tee data/output_sarl_bl1/eval/multi-lg-sq
    """
    
    test_envs = [
        "bl-cr",
        "bl-sq",
        "dn-cr",
        "dn-sq",
        "lg-cr",
        "lg-sq"
    ]
    
    gpu_str = "--gpu" if gpu else ""
    #os.system("at now + ")
    cmd = ""
    for i, env in enumerate(test_envs):
        cmd += f"python test.py --policy {policy} --phase test --model_dir data/{model_dir} --env_config configs/env_multi-test_{env}.config {gpu_str} 2>&1 | tee data/{model_dir}/eval/multi-{env}"
        if i != len(test_envs) - 1:
            cmd += " & \n wait; "
    
    os.system(cmd)
