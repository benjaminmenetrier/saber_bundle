#!/usr/bin/env python3

import os
import copy
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess

# Parameters
rho = 8.0
rmean = 0.06
rvar = 0.04
ndir = 6

# Non-adaptative
xh = np.array([0.0])
rh = np.array([rmean])
ri = np.array([rmean-rvar])
nh = 1
dxh = rmean/rho
while xh[nh-1] < 1.0:
  xh = np.append(xh, xh[nh-1]+dxh)
  rh = np.append(rh, rmean)
  ri = np.append(ri, rmean-rvar*np.cos(2.0*math.pi*xh[nh]))
  nh += 1

# Adaptative
xa = np.array([0.0])
ra = np.array([rmean-rvar])
na = 1
while xa[na-1] < 1.0:
  dx = (rmean-rvar*np.cos(2.0*math.pi*xa[na-1]))/rho
  xa = np.append(xa, xa[na-1]+dx)
  ra = np.append(ra, rmean-rvar*np.cos(2.0*math.pi*xa[na]))
  na += 1

# Dirac vector
xdir = np.linspace(0.5/ndir, 1.0-0.5/ndir, ndir)

# Convolution function
def gc99_sqrt(x, yin, r):
  n = len(x)
  yout = np.zeros((n))
  for i in range(n):
    for j in range(n):
      d = np.abs(x[i]-x[j])
      if (d > 0.5):
        d = 1.0-d
      d /= r[i]
      if d < 0.5:
        yout[i] += (1.0-2.0*d)*yin[j]
  return yout

# Normalization function
def norm(x, r):
  n = len(x)
  norm = np.zeros((n))
  for i in range(n):
    test = np.zeros((n))
    test[i] = 1.0
    test = gc99_sqrt(x, test, r)
    norm[i] = 1.0/np.sqrt(np.sum(test*test))
  return norm

# Compute normalization
normh = norm(xh, rh)
normi = norm(xh, ri)
norma = norm(xa, ra)

# Dirac locations
ydirh = np.zeros((nh))
idir = 0
for i in range(nh):
  if idir < ndir:
    if xh[i] > xdir[idir]:
      if xdir[idir]-xh[i-1] < xh[i]-xdir[idir]:
        ydirh[i-1] = 1.0
      else:
        ydirh[i] = 1.0
      idir += 1
ydira = np.zeros((na))
idir = 0
for i in range(na):
  if idir < ndir:
    if xa[i] > xdir[idir]:
      if xdir[idir]-xa[i-1] < xa[i]-xdir[idir]:
        ydira[i-1] = 1.0
      else:
        ydira[i] = 1.0
      idir += 1

# Apply convolution function
yh1 = ydirh*normh
yh1 = gc99_sqrt(xh, yh1, rh)
yh2 = gc99_sqrt(xh, yh1, rh)
yh2 = yh2*normh

yi1 = ydirh*normi
yi1 = gc99_sqrt(xh, yi1, ri)
yi2 = gc99_sqrt(xh, yi1, ri)
yi2 = yi2*normi

ya1 = ydira*norma
ya1 = gc99_sqrt(xa, ya1, ra)
ya2 = gc99_sqrt(xa, ya1, ra)
ya2 = ya2*norma

# Local resolution
rhoh = np.full((nh), rho)
rhoi = ri/dxh
rhoa = np.full((na), rho)

# Rescale x / xa
xh *= 2.0
xa *= 2.0
rh *= 2.0
ri *= 2.0
ra *= 2.0

# Plot curves

# rh
fig, ax = plt.subplots(nrows=4, figsize=(10,8))
ax[0].set_xlim([0.0,1.0])
ax[0].set_ylim([0,0.25])
ax[0].set_ylabel("Support radius r", color='b')
ax[0].tick_params(axis ='y', labelcolor='b')
ax[0].plot(xh, rh, 'b', marker='s', markersize=4.0, linewidth=0.5) 
ax_right = ax[0].twinx()
ax_right.set_xlim([0.0,1.0])
ax_right.set_ylim([0.0,0.125/dxh])
ax_right.set_ylabel(r"Resolution $\widehat{\rho}$", color='r')
ax_right.plot(xh, rhoh, 'r', marker='o', markersize=2.0, linewidth=0.5)
ax_right.tick_params(axis ='y', labelcolor='r') 

ax[1].set_xlim([0.0,1.0])
ax[1].set_ylim([0,1.1])
ax[1].set_ylabel(r"$\boldsymbol{\delta}$")
ax[1].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[1].plot(xh, ydirh, "k", marker='o', markersize=2.0, linewidth=0.5)

ax[2].set_xlim([0.0,1.0])
ax[2].set_ylim([0,1.1])
ax[2].set_ylabel(r"$\widehat{\mathbf{U}}^\mathrm{T} \boldsymbol{\delta}$")
ax[2].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[2].plot(xh, yh1, "k", marker='o', markersize=2.0, linewidth=0.5)

ax[3].set_xlim([0.0,1.0])
ax[3].set_ylim([0,1.1])
ax[3].set_ylabel(r"$\widehat{\mathbf{C}} \boldsymbol{\delta}$")
ax[3].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[3].plot(xh, yh2, "k", marker='o', markersize=2.0, linewidth=0.5)

filename = 'gc99_rh'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])

# ri
fig, ax = plt.subplots(nrows=4, figsize=(10,8))
ax[0].set_xlim([0.0,1.0])
ax[0].set_ylim([0,0.25])
ax[0].set_ylabel("Support radius r", color='b')
ax[0].plot(xh, ri, 'b', marker='s', markersize=4.0, linewidth=0.5)
ax[0].tick_params(axis ='y', labelcolor='b') 
ax_right = ax[0].twinx()
ax_right.set_xlim([0.0,1.0])
ax_right.set_ylim([0.0,0.125/dxh])
ax_right.set_ylabel(r"Resolution $\widehat{\rho}$", color='r')
ax_right.plot(xh, rhoi, 'r', marker='o', markersize=2.0, linewidth=0.5)
ax_right.tick_params(axis ='y', labelcolor='r') 

ax[1].set_xlim([0.0,1.0])
ax[1].set_ylim([0,1.1])
ax[1].set_ylabel(r"$\boldsymbol{\delta}$")
ax[1].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[1].plot(xh, ydirh, "k", marker='o', markersize=2.0, linewidth=0.5)

ax[2].set_xlim([0.0,1.0])
ax[2].set_ylim([0,1.1])
ax[2].set_ylabel(r"$\widehat{\mathbf{U}}^\mathrm{T} \boldsymbol{\delta}$")
ax[2].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[2].plot(xh, yi1, "k", marker='o', markersize=2.0, linewidth=0.5)

ax[3].set_xlim([0.0,1.0])
ax[3].set_ylim([0,1.1])
ax[3].set_ylabel(r"$\widehat{\mathbf{C}} \boldsymbol{\delta}$")
ax[3].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[3].plot(xh, yi2, "k", marker='o', markersize=2.0, linewidth=0.5)

filename = 'gc99_ri'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])

# ra
fig, ax = plt.subplots(nrows=4, figsize=(10,8))
ax[0].set_xlim([0.0,1.0])
ax[0].set_ylim([0,0.25])
ax[0].set_ylabel("Support radius r", color='b')
ax[0].plot(xa, ra, 'b', marker='s', markersize=4.0, linewidth=0.5)
ax[0].tick_params(axis ='y', labelcolor='b') 
ax_right = ax[0].twinx()
ax_right.set_xlim([0.0,1.0])
ax_right.set_ylim([0.0,0.125/dxh])
ax_right.set_ylabel(r"Resolution $\widehat{\rho}$", color='r')
ax_right.plot(xa, rhoa, 'r', marker='o', markersize=2.0, linewidth=0.5)
ax_right.tick_params(axis ='y', labelcolor='r') 

ax[1].set_xlim([0.0,1.0])
ax[1].set_ylim([0,1.1])
ax[1].set_ylabel(r"$\boldsymbol{\delta}$")
ax[1].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[1].plot(xa, ydira, "k", marker='o', markersize=2.0, linewidth=0.5)

ax[2].set_xlim([0.0,1.0])
ax[2].set_ylim([0,1.1])
ax[2].set_ylabel(r"$\widehat{\mathbf{U}}^\mathrm{T} \boldsymbol{\delta}$")
ax[2].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[2].plot(xa, ya1, "k", marker='o', markersize=2.0, linewidth=0.5)

ax[3].set_xlim([0.0,1.0])
ax[3].set_ylim([0,1.1])
ax[3].set_ylabel(r"$\widehat{\mathbf{C}} \boldsymbol{\delta}$")
ax[3].axhline(y=1.0, color='gray', linewidth=0.5, linestyle=':')
ax[3].plot(xa, ya2, "k", marker='o', markersize=2.0, linewidth=0.5)

filename = 'gc99_ra'
plt.savefig('../fig/' + filename + '.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/' + filename + '.pdf', '../fig/' + filename + '.pdf'])
