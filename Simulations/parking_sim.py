# A script to simulate the parking process on a graph.

import random
import numpy
import copy
from math import *
import matplotlib.pyplot as plt

# Let's introduce the basic parking process dynamics on Z/NZ, starting with probability p of having a car, and all remaining sites
# are parking spots.

# Generate an initial configuration vector on Z/NZ. +1 represents a car, while -1 will represent a parking spot. So we reserve
# 0 for a spot that initially had a car, but is vacant, or a spot that was filled by a car.

# 'Variant' index: p = standard parking, pa = parking with annihilation, pc = parking with coalescence,
# pb = parking with branching, pba = parking with branching and annihilation, pbc = parking with branching and coalescence.

# Not sure that

# A function to return a random index sampled from a vector [p_0, p_1, ... p_n]. Namely, return i with probability p_i / sum(p_i).
def discrete_sample(vec):
    nonneg_vec = copy.copy(vec)
    for i in range(len(vec)):
        if vec[i] < 0:
            nonneg_vec[i] = 0

    a = random.random()
    s = sum(nonneg_vec)
    b = nonneg_vec[0] / s
    i = 0
    while b < a:
        i += 1
        b += nonneg_vec[i] / s
    return(i)


class config:
    def __init__(self, N, p, variant):
        self.length = N
        self.carprob = p
        self.variant = variant
        self.state = []
        self.cars = 0
        self.spots = 0

        # Generate the initial configuration.
        j = 0
        while j < N:
            j += 1
            w = random.random()
            if w < p:
                self.state.append(1)
                self.cars += 1
            else:
                self.state.append(-1)
                self.spots += 1

    # A car at site i parks at site j.
    def park(self, i, j):
        self.state[i] -= 1
        self.state[j] = 0
        self.cars -= 1
        self.spots -= 1

    # A car at site i annihilates a car at site j.
    def annihilate(self, i, j):
        self.state[i] -= 1
        self.state[j] -= 1
        self.cars -= 2

    # A car at site i coalesces with cars at site j.
    def coalesce(self, i, j):
        self.state[i] -= 1
        self.cars -= 1

    # A car at site i drives to site j.
    def drive(self, i, j):
        self.state[i] -= 1
        self.state[j] += 1

    # Update the configuration by toppling at a random site.
    def topple(self):
        if self.cars == 0:
            # print('stable')
            return False
        else:
            x = discrete_sample(self.state)

            w = random.random()
            if w < 1 / 2:
                y = (x + 1) % self.length
            else:
                y = (x - 1) % self.length

            target = self.state[y]

            if self.variant == 'p':
                if target == -1:
                    self.park(x,y)
                else:
                    self.drive(x,y)

            elif self.variant == 'pa':
                if target == -1:
                    self.park(x,y)

                elif target == 0:
                    self.drive(x,y)

                elif target == 1:
                    self.annihilate(x,y)

            elif self.variant == 'pc':
                if target == -1:
                    self.park(x,y)

                elif target == 0:
                    self.drive(x,y)

                elif target > 0:
                    self.coalesce(x,y)

            return True


# Statistical test for criticality. Vary the value of p, and check: did every spot eventually get parked in?
def criticality_stats(N, delta_p, pmin, pmax, trials, variant):
    p_range = int((pmax - pmin) * delta_p**(-1))
    parked_data = [0] * p_range
    for j in range(p_range):
        p = pmin + j * delta_p
        print(p)
        for s in range(int(trials)):
            u = config(N, p, variant)
            while u.spots > 0 and u.cars > 0:
                u.topple()

            if u.spots == 0:
                parked_data[j] += 1.0 / trials

    return parked_data



# Run a single instance of the process. Good for debugging.
def single_sim(N, p, variant):
    u = config(N, p, variant)
    print(u.state)
    while u.spots > 0 and u.cars > 0:
        u.topple()
        print(u.state, u.spots, u.cars)


# How does the number of active cars decay over time?
def odometer_stats(N, p, T, trials, variant):
    density_data = [0] * T
    for s in range(trials):
        u = config(N, p, variant)
        for t in range(T):
            density_data[t] += u.cars / (N * trials)
            u.topple()

    return(density_data)

# Odometer stat calculator, for various values of p.
# N = 30
# T = 200
# trials = 1000
# data = odometer_stats(N, .5, T, trials, 'p')
# data2 = odometer_stats(N, .45, T, trials, 'p')
# data3 = odometer_stats(N, .2, T, trials, 'p')
# data4 = odometer_stats(N, .75, T, trials, 'p')
# plt.plot(range(T), data, 'r', range(T), data2, 'b', range(T), data3, 'g', range(T), data4, 'm')
# plt.show()

# # Critical window plot.
a = .7
b = .9
dp = .02
N = 2000
T = 5

data = criticality_stats(N, dp, a, b, T, 'pc')
plt.plot(data)
plt.show()

# Crit stats with N = 2000 and T = 5 gave P(all spots dead) ~ .5 when p ~ .785.

########################################################################################################################
########################################################################################################################
#Networkx experimentation###############################################################################################
########################################################################################################################
########################################################################################################################

import networkx as nx
G = nx.Graph()

# TODO: parking process given an arbitrary adjacency matrix...