#!/usr/bin/env python3

import os
import copy
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess

# Parameters range
mpiVec = np.array([16,32,64,128])

# Load data
nMpi = len(mpiVec)
setup_timing = np.zeros((nMpi, 4))
app_timing = np.zeros((nMpi, 5))
for i in range(nMpi):
  datafile = "../data/timing/timing_" + str(mpiVec[i]) + "_20_8_c0_regular/timing_" + str(mpiVec[i]) + "_20_8_c0_regular.txt"
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
x = np.linspace(0, nMpi-1, nMpi)
xticks = x
xlbls = mpiVec

# Plot
fig, ax = plt.subplots(nrows=2, figsize=(5,9), sharex=True)
width = 0.9
setup_timing = setup_timing*1.0e-3
for i in range(4):
  ax[0].bar(x, setup_timing[:,i], width, bottom=np.sum(setup_timing[:,0:i],axis=1))
opt_scalability = np.sum(setup_timing[0,:])*mpiVec[0]/mpiVec
ax[0].plot(x, opt_scalability, 'k--', marker='o')
ax[0].set_ylabel("Setup elapsed time (s)")
ax[0].legend(['Extrapolated scalability', 'Subgrid generation','Interpolation setup','Convolution setup','Normalization setup'], loc='upper right') 
ax[0].set_ylim([0.0,35.0])
for i in range(5):
  ax[1].bar(x, app_timing[:,i], width, bottom=np.sum(app_timing[:,0:i],axis=1))
opt_scalability = np.sum(app_timing[0,:])*mpiVec[0]/mpiVec
ax[1].plot(x, opt_scalability, 'k--', marker='o')
ax[1].set_xlabel("Number of MPI tasks")
ax[1].set_ylabel("Application elapsed time (ms)")
ax[1].set_ylim([0.0,39.5])
ax[1].set_xticks(xticks)
ax[1].set_xticklabels(xlbls)
ax[1].tick_params(axis='both', which='both', length=0)
ax[1].legend(['Extrapolated scalability','Interpolation (application)','Interpolation (communication)','Convolution (application)','Convolution (communication)','Normalization'], loc='upper right') 
fig.subplots_adjust(hspace=0)
filename = 'timing_scalability'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])
