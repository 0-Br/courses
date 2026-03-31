import numpy as np
from matplotlib import pyplot as plt

INFO = "(0, v1)"

hist_loss_REINFORCE = np.load("./cache/hist_loss_REINFORCE %s.npy" % INFO)
hist_reward_REINFORCE = np.load("./cache/hist_reward_REINFORCE %s.npy" % INFO)
hist_loss_TDAC = np.load("./cache/hist_loss_TDAC %s.npy" % INFO)
hist_reward_TDAC = np.load("./cache/hist_reward_TDAC %s.npy" % INFO)

num_loss = len(hist_loss_REINFORCE)
num_reward = len(hist_reward_REINFORCE)

plt.figure(figsize=(9, 9), dpi=400)
plt.xlabel('episode_id')
plt.ylabel('reward')
plt.plot(range(num_reward), hist_reward_REINFORCE, linewidth=1, label="REINFORCE")
plt.plot(range(num_reward), hist_reward_TDAC, linewidth=1, label="TDActorCritic")
plt.legend()
plt.savefig("reward %s.png" % INFO)

plt.figure(figsize=(9, 9), dpi=400)
plt.xlabel('episode_id')
plt.ylabel('loss')
plt.plot(range(num_loss), hist_loss_REINFORCE, linewidth=1, label="REINFORCE")
plt.legend()
plt.savefig("loss_REINFORCE %s.png" % INFO)

plt.figure(figsize=(9, 9), dpi=400)
plt.xlabel('episode_id')
plt.ylabel('loss')
plt.plot(range(num_loss), hist_loss_TDAC, linewidth=1, label="TDActorCritic")
plt.legend()
plt.savefig("loss_TDAC %s.png" % INFO)

