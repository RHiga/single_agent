from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import math

class ELAgent():

    def __init__(self, epsilon):
        self.Q = {}
        self.epsilon = epsilon
        self.reward_log = []

    def policy(self, s, actions):
        if np.random.random() < self.epsilon:
            return np.random.randint(len(actions))
        else:
            if s in self.Q and sum(self.Q[s]) != 0:
                return np.argmax(self.Q[s])
            else:
                return np.random.randint(len(actions))

    def init_log(self):
        self.reward_log = []

    def log(self, reward):
        self.reward_log.append(reward)

    def show_reward_log(self, interval=100, episode=-1):
        if episode > 0:
            rewards = self.reward_log[-interval:]
            mean = np.round(np.mean(rewards), 3)
            std = np.round(np.std(rewards), 3)
            print("At Episode {} average reward is {} (+/-{}).".format(
                   episode, mean, std))
        else:
            indices = list(range(0, len(self.reward_log), interval))
            means = []
            stds = []
            for i in indices:
                rewards = self.reward_log[i:(i + interval)]
                means.append(np.mean(rewards))
                stds.append(np.std(rewards))
            means = np.array(means)
            stds = np.array(stds)
            plt.figure()
            plt.title("Reward History")
            plt.grid()
            plt.fill_between(indices, means - stds, means + stds,
                             alpha=0.1, color="g")
            plt.plot(indices, means, "o-", color="g",
                     label="Rewards for each {} episode".format(interval))
            plt.legend(loc="best")
            plt.show()

class QLearningAgent(ELAgent):

    def __init__(self, epsilon=0.01):
        super().__init__(epsilon)

    # observation function
    def observation(self, s, env):
        return s.row*env.column_length + s.column + s.agv_stock*env.row_length*env.column_length


    def learn(self, env, episode_count=1000, gamma=0.98,
              learning_rate=0.1, render=False, report_interval=100):
        self.init_log()
        actions = list(range(env.actions_length))

        self.Q = defaultdict(lambda: [0] * len(actions))
        for e in range(episode_count):
            s = env.reset()
            done = False
            while not done:

                #a = self.policy(s, actions)
                obs = self.observation(s, env)
                a = self.policy(obs, actions)

                n_state, reward, done = env.step(env.actions[a])

                n_obs = self.observation(n_state, env)

                #gain = reward + gamma * max(self.Q[n_state])
                gain = reward + gamma * max(self.Q[n_obs])

                obs = self.observation(s, env)

                #estimated = self.Q[s][a]
                estimated = self.Q[obs][a]
                #self.Q[s][a] += learning_rate * (gain - estimated)
                self.Q[obs][a] += learning_rate * (gain - estimated)

                s = n_state

            else:
                self.log(reward)

            if e != 0 and e % report_interval == 0:
                self.show_reward_log(episode=e)

class QLearningAgentOrign(ELAgent):

    def __init__(self, epsilon=0.1):
        super().__init__(epsilon)

    def learn(self, env, episode_count=1000, gamma=0.98,
              learning_rate=0.1, render=False, report_interval=100):
        self.init_log()
        actions = list(range(env.actions_length))

        self.Q = defaultdict(lambda: [0] * len(actions))
        for e in range(episode_count):
            s = env.reset()
            done = False
            while not done:

                a = self.policy(s, actions)

                estimated = self.Q[s][a]

                n_state, reward, done = env.step(env.actions[a])


                gain = reward + gamma * max(self.Q[n_state])

                estimated = self.Q[s][a]

                self.Q[s][a] += learning_rate * (gain - estimated)

                s = n_state

            else:
                self.log(reward)

            if e != 0 and e % report_interval == 0:
                self.show_reward_log(episode=e)

class MonteCarloAgent(ELAgent):

    def __init__(self, epsilon=0.1):
        super().__init__(epsilon)

    def learn(self, env, episode_count=1000, gamma=0.98,
              render=False, report_interval=100):
        self.init_log()
        actions = list(range(env.actions_length))
        self.Q = defaultdict(lambda: [0] * len(actions))
        N = defaultdict(lambda: [0] * len(actions))

        for e in range(episode_count):
            s = env.reset()
            done = False
            # Play until the end of episode.
            experience = []
            while not done:

                a = self.policy(s, actions)
                n_state, reward, done = env.step(env.actions[a])

                experience.append({"state": s, "action": a, "reward": reward})
                s = n_state
            else:
                self.log(reward)

            # Evaluate each state, action.
            for i, x in enumerate(experience):
                s, a = x["state"], x["action"]

                # Calculate discounted future reward of s.
                G, t = 0, 0
                for j in range(i, len(experience)):
                    G += math.pow(gamma, t) * experience[j]["reward"]
                    t += 1

                N[s][a] += 1  # count of s, a pair
                alpha = 1 / N[s][a]
                self.Q[s][a] += alpha * (G - self.Q[s][a])

            if e != 0 and e % report_interval == 0:
                self.show_reward_log(episode=e)
