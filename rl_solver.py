
from datetime import datetime
from pathlib import Path

import ray.tune
from ray.rllib.algorithms.ppo import PPOConfig, PPO
from ray.rllib.env import EnvContext
from ray.rllib.callbacks.callbacks import RLlibCallback

from env.game_gym import Game6NimmtEnv

# Own metric for tensor view
class PenaltyMetricsCallback(RLlibCallback):
    def on_episode_end(self, *, episode, metrics_logger=None, **kwargs):
        # Get the last step's info dict (single-agent new stack)
        last_info = episode.get_infos(-1)
        if last_info and "penalty" in last_info:
            metrics_logger.log_value("final_penalty", float(last_info["penalty"]))
        if last_info and "rank" in last_info:
            metrics_logger.log_value("final_rank", float(last_info["rank"]))


def env_create(env_config: EnvContext):
    return Game6NimmtEnv(**env_config)


def print_ppo_configs(config):
    print("Ray Version:", ray.__version__)
    print("clip_param", config.clip_param)
    print("gamma", config.gamma)
    print("lr", config.lr)
    print("lamda", config.lambda_)


def grid_search_hypers(env_params: dict, nn_model: list, activation: str, gammas: list, desc: str, train_hw: dict, use_lstm: bool):
    ray.tune.register_env("Game6NimmtEnv", env_create)

    config = PPOConfig()

    config = config.framework(framework='torch')
    config = config.resources(num_gpus=train_hw["gpu"])
    config = config.environment(env="Game6NimmtEnv", env_config=env_params)

    config = config.rl_module(
        model_config={
            "fcnet_hiddens": nn_model,
            "fcnet_activation": activation,
        }
    )

    if use_lstm:
        config = config.rl_module(
            model_config={
                "use_lstm": True,
                "max_seq_len": 20,
                "lstm_cell_size": 256,
                "lstm_use_prev_reward": False,
                "lstm_use_prev_action": False,
            }
        )

    config = config.env_runners(num_env_runners=train_hw["cpu"])
    config = config.training(gamma=ray.tune.grid_search(gammas))
    config = config.callbacks(PenaltyMetricsCallback)
    config = config.debugging(log_level="ERROR")
    experiment_name = f"PPO_{desc}_{datetime.now():%Y-%m-%d_%H-%M}_MODEL={nn_model}_ACT={activation}"

    storage_uri = Path("out").resolve().as_uri()

    tuner = ray.tune.Tuner(
        trainable=PPO,
        param_space=config.to_dict(),
        run_config=ray.tune.RunConfig(
            name=experiment_name,
            storage_path=storage_uri,
            verbose=2,
            stop=ray.tune.stopper.MaximumIterationStopper(100),
            checkpoint_config=ray.tune.CheckpointConfig(checkpoint_frequency=200)
        )
    )

    tuner.fit()


def resume_training():
    # restore checkpoint and resume learning
    # rsc: https://discuss.ray.io/t/unable-to-restore-fully-trained-checkpoint/8259/8
    # rsc: https://github.com/ray-project/ray/issues/4569
    # Note: The call works, but training does not continue (max iter reached?!)
    tuner = Tuner.restore("out/PPO_SmartBomber-DeadNearBomb-LongTraining-Gamma-0.75_2023-05-17_07-41_MODEL=[512, 512, 256, 128, 64]_ACT=relu")
    tuner.fit()


if __name__ == '__main__':

    # training settings
    hw = {"gpu": 1, "cpu": 10}
    env_params = {}
    nn_model = [128, 128, 64]
    activation = "relu"
    description = "Test6Nimmt"
    gammas = [0.75, 0.80, 0.9, 0.99]

    grid_search_hypers(env_params, nn_model, activation, gammas, description, hw, use_lstm=True)
