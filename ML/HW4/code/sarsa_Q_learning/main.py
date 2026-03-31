import gym
import random
import numpy as np
import matplotlib.pyplot as plt
from algorithms import QLearning, Sarsa
from utils import render_single_Q, evaluate_Q


# Feel free to run your own debug code in main!
def main(lr):

    SEED = 42
    random.seed(SEED)
    np.random.seed(SEED)

    num_episodes = 10000
    env = gym.make('Taxi-v3')

    print("#" * 128)
    print("lr: %.4f" % lr)

    # q_learning
    Q1, Q1_rewards = QLearning(env, num_episodes, lr=lr)
    # render_single_Q(env, Q1)
    evaluate_Q(env, Q1, 200)

    # Sarsa
    Q2, Q2_rewards = Sarsa(env, num_episodes, lr=lr)
    # render_single_Q(env, Q2)
    evaluate_Q(env, Q2, 200)

    plt.figure(figsize=(15, 6), dpi=400)
    plt.xlabel('episode_id')
    plt.ylabel('reward')
    plt.plot(range(num_episodes), Q1_rewards, linewidth=0.5, label="QLearning")
    plt.plot(range(num_episodes), Q2_rewards, linewidth=0.5, label="Sarsa")
    plt.legend()
    plt.savefig("main(lr=%.4f).png" % lr)

    np.save("reward_QLearning(lr=%.4f).npy" % lr, Q1_rewards)
    np.save("reward_Sarsa(lr=%.4f).npy" % lr, Q2_rewards)

    print("#" * 128)
    print()


if __name__ == '__main__':
    for lr in (0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10):
        main(lr=lr)
