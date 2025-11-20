#!/usr/bin/env python3

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import subprocess

# Define domain
nx = 1001
x = np.linspace(-1.0, 1.0, nx)

# Components
a = [0.15,0.3,0.55]
rh = [1.0,0.45,0.2]
colors = ['b','r','g']

# Convolution function
def gc99(d):
  if (np.abs(d) < 0.5):
    out = 1-8*d**5+8*d**4+5*d**3-20/3*d**2
  elif d < 1.0:
    out = 8/3*d**5-8*d**4+5*d**3+20/3*d**2-10*d+4-1/(3*d)
  else:
    out = 0.0
  return out

# Compute components
ysep = np.zeros((nx,3))
for jc in range(3):
  for jx in range(nx):
    d = abs(x[jx])/rh[jc]
    ysep[jx,jc] = a[jc]*gc99(d)

# Add components
ysum = np.zeros((nx,3))
ysum[:,0] = ysep[:,0]
ysum[:,1] = ysum[:,0]+ysep[:,1]
ysum[:,2] = ysum[:,1]+ysep[:,2]

# Plot
os.makedirs("../fig", exist_ok=True)
fig, ax = plt.subplots(nrows=2, figsize=(6,6), sharex=True)
ax[0].set_xlim([-1.0,1.0])
ax[0].set_ylim([0,0.6])
ax[0].set_ylabel("Independent commponents")
for jc in range(3):
  ax[0].plot(x, ysep[:,jc], color=colors[jc], linewidth=2.0)
ax[1].set_xlim([-1.0,1.0])
ax[1].set_ylim([0,1.15])
ax[1].set_ylabel("Accumulated commponents")
for jc in range(3):
  ax[1].plot(x, ysum[:,jc], color=colors[jc], linewidth=2.0)
ax[1].fill_between(x, ysum[:,0], color='b', alpha=0.5)
ax[1].fill_between(x, ysum[:,1], ysum[:,0], color='r', alpha=0.5)
ax[1].fill_between(x, ysum[:,2], ysum[:,1], color='g', alpha=0.5)
ax[1].set_xticklabels([])

fig.subplots_adjust(hspace=0)
filename = 'multicmp'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])
