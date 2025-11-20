#!/usr/bin/env python3

import os
import copy
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess

# Parameters range
interpVec = ["c0","c1","si"]
xlbls = ["C0","C1","Smoothing"]

# Load data
nInterp = len(interpVec)
setup_timing = np.zeros((nInterp, 4))
app_timing = np.zeros((nInterp, 5))
for i in range(nInterp):
  datafile = "../data/timing/timing_32_20_8_" + interpVec[i] + "_regular/timing_32_20_8_" + interpVec[i] + "_regular.txt"
  data = np.zeros((9))
  if os.path.exists(datafile):
    with open(datafile, "r") as f:
      l = 0
      for line in f:
        data[l] = float(line.strip().split()[10])
        l += 1

    # Setup timing
    for l in range(4):
      setup_timing[i,l] = data[l]

    # Application timing
    for l in range(5):
      app_timing[i,l] = data[4+l]
  else:
    setup_timing[i,:] = 0.0
    app_timing[i,:] = 0.0

# Timing ticks
x = np.linspace(0, nInterp-1, nInterp)
xticks = x

# Plot
fig, ax = plt.subplots(nrows=2, figsize=(5.5,9), sharex=True)
width = 0.9
setup_timing = setup_timing*1.0e-3
for i in range(4):
  ax[0].bar(x, setup_timing[:,i], width, bottom=np.sum(setup_timing[:,0:i],axis=1))
ax[0].set_ylabel("Setup elapsed time (s)")
ax[0].legend(['Subgrid generation','Interpolation setup','Convolution setup','Normalization setup'], loc='upper left') 
ax[0].set_ylim([0.0,40.0])
for i in range(5):
  ax[1].bar(x, app_timing[:,i], width, bottom=np.sum(app_timing[:,0:i],axis=1))
ax[1].set_xlabel("Interpolation type")
ax[1].set_ylabel("Application elapsed time (ms)")
ax[1].set_ylim([0.0,39.5])
ax[1].set_xticks(xticks)
ax[1].set_xticklabels(xlbls)
ax[1].tick_params(axis='both', which='both', length=0)
ax[1].legend(['Interpolation (application)','Interpolation (communication)','Convolution (application)','Convolution (communication)','Normalization'], loc='upper left') 
fig.subplots_adjust(hspace=0)
filename = 'timing_interp'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])
