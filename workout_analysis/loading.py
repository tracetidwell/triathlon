# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 07:30:16 2017

@author: Trace
"""

import numpy as np
import math
import matplotlib.pyplot as plt

nF = 42
lambdaF = math.exp(-1/nF)

nA = 7
lambdaA = math.exp(-1/nA)

#if_ = np.array([0.6] * 112 + [0.7] * 112 + [0.8] * 84)
if_ = np.array([0.65, 0.65, 0.65, 0.73, 0.69, 0.69, 0.76, 0.71, 0.71, 0.78, 0.81])
#load = np.array([40] * 56 + [50] * 56 + [60] * 56 + [70] * 28 + [50] * 84 + [40] * 28)
volume = np.array([40, 46, 53, 42, 52, 58, 48, 60, 60, 53, 40])

#tss = if_**2 * 100 * load / 28

ctl = np.zeros(len(volume)*28+1)
ctl[0] = 30

atl = np.zeros(len(volume)*28+1)
atl[0] = 30

tsb = np.zeros(len(volume)*28+1)
tsb[0] = 0

split = np.array([.155, .25, 0.07, .135, .15, .09, .15])

for i in range(11):
    for j in range(1, 22):
        load = np.array([0, 0, 30, 0, 0, 30, 0]) + (if_[i]**2 * 100 * volume[i]/4) * split
        ctl[i*28 + j] = load[j%7] * (1 - lambdaF) + ctl[i*28 + j-1] * lambdaF
        atl[i*28 + j] = load[j%7] * (1 - lambdaA) + atl[i*28 + j-1] * lambdaA
        tsb[i*28 + j] = ctl[i*28 + j] - atl[i*28 + j]
    floor = min(tsb[i:i+28])
    for j in range(22, 29):
        load = np.array([0, 0, 30, 0, 0, 30, 0]) + (floor + ctl[i*28 + j-1]) * split * 7
        ctl[i*28 + j] = load[j%7] * (1 - lambdaF) + ctl[i*28 + j-1] * lambdaF
        atl[i*28 + j] = load[j%7] * (1 - lambdaA) + atl[i*28 + j-1] * lambdaA
        tsb[i*28 + j] = ctl[i*28 + j] - atl[i*28 + j]
            

#for i in range(1, len(ctl)):
#    ctl[i] = tss[i-1] * (1 - lambdaF) + ctl[i-1] * lambdaF
#    atl[i] = tss[i-1] * (1 - lambdaA) + ctl[i-1] * lambdaA
#
#tsb = np.zeros(len(load))
#tsb = ctl[1:] - atl[1:]
#
plt.plot(ctl)
print(ctl[-1])
#plt.plot(tsb)