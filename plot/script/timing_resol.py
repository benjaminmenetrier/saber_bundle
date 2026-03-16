#!/usr/bin/env python3

import os
import copy
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess

# Parameters ranges
ratioVec = np.array([30,20,10])
resolVec = np.array([4,6,8,10])

# Load data
nRatio = len(ratioVec)
nResol = len(resolVec)
setup_timing = np.zeros((nRatio*nResol, 4))
app_timing = np.zeros((nRatio*nResol, 5))
for i in range(nRatio):
  for j in range(nResol):
    datafile = "../data/timing/timing_32_" + str(ratioVec[i]) + "_" + str(resolVec[j]) + "_c0_regular/timing_32_" + str(ratioVec[i]) + "_" + str(resolVec[j]) + "_c0_regular.txt"
    data = np.zeros((9))
    if os.path.exists(datafile):
      with open(datafile, "r") as f:
        l = 0
        for line in f:
          data[l] = float(line.strip().split()[10])
          l += 1

      # Setup timing
      for l in range(4):
        setup_timing[i*nResol+j,l] = data[l]

      # Application timing
      for l in range(5):
        app_timing[i*nResol+j,l] = data[4+l]
    else:
      setup_timing[i*nResol+j,:] = 0.0
      app_timing[i*nResol+j,:] = 0.0

# Timing ticks
x = np.zeros((nRatio*nResol))
xticks = []
xlbls = []
va = []
for i in range(nRatio):
  for j in range(nResol):
    x[i*nResol+j] = float(i*(nResol+1)+j)
    if j-1 < (nResol-1)/2 and (nResol-1)/2 < j:
      xticks.append(float(i*(nResol+1)+(nResol-1)/2))
      xlbls.append(r"$\rho =$" + str(ratioVec[i]))
      va.append(-0.05)
    xticks.append(float(i*(nResol+1)+j))
    xlbls.append(resolVec[j])
    va.append(0.0)

# Timing x-axis label
xticks.append(xticks[len(xticks)-1]+1.2)
xlbls.append(r"$\widehat{\rho}$")
va.append(0.0)

# Plot
fig, ax = plt.subplots(nrows=2, figsize=(8,8), sharex=True)
width = 0.9
setup_timing = setup_timing*1.0e-3
for i in range(4):
  ax[0].bar(x, setup_timing[:,i], width, bottom=np.sum(setup_timing[:,0:i],axis=1))
ax[0].set_ylabel("Setup elapsed time (s)")
ax[0].set_ylim([0.0,85.0])
ax[0].legend(['Subgrid generation','Interpolation setup','Convolution setup','Normalization setup'], loc='upper left')  
for i in range(5):
  ax[1].bar(x, app_timing[:,i], width, bottom=np.sum(app_timing[:,0:i],axis=1))
ax[1].set_ylabel("Application elapsed time (ms)")
ax[1].set_ylim([0.0,31.9])
ax[1].set_xticks(xticks)
ax[1].set_xticklabels(xlbls)
for t, y in zip(ax[1].get_xticklabels( ), va):
  t.set_y(y)
ax[1].tick_params(axis='both', which='both', length=0)
ax[1].legend(['Interpolation (computation)','Interpolation (communication)','Convolution (computation)','Convolution (communication)','Normalization'], loc='upper left') 
fig.subplots_adjust(hspace=0)
filename = 'timing_resol'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])
