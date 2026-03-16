#!/usr/bin/env python3

import copy
import os
import matplotlib.pylab as plt
import numpy as np
import subprocess
from mpl_toolkits.mplot3d import Axes3D

# Figures repository
os.makedirs("../fig", exist_ok=True)

# Define full grid
dxf = 0.025
dyf = dxf*np.sqrt(2.0/3.0)
xf = np.arange(0.0, 1.0, dxf)
yf = np.arange(0.0, 1.0, dyf)
zf1 = np.linspace(0.0, 1.0, 7)
zf2 = zf1[[0,2,6]]
nxf = len(xf)
nyf = len(yf)
nzf1 = len(zf1)
nzf2 = len(zf2)
xfplot1 = []
yfplot1 = []
zfplot1 = []
xfplot2 = []
yfplot2 = []
zfplot2 = []
for iz in range(nzf1):
  for iy in range(nyf):
    for ix in range(nxf):
      if iy%2 == 0:
        xfplot1.append(xf[ix])
      else:
        xfplot1.append(xf[ix]+0.5/float(nxf-1))
      yfplot1.append(yf[iy])
      zfplot1.append(zf1[iz])
for iz in range(nzf2):
  for iy in range(nyf):
    for ix in range(nxf):
      if iy%2 == 0:
        xfplot2.append(xf[ix])
      else:
        xfplot2.append(xf[ix]+0.5/float(nxf-1))
      yfplot2.append(yf[iy])
      zfplot2.append(zf2[iz])

# Define reduced grids
sr = np.linspace(2.0, 16.0, nzf2)
dxr = np.linspace(0.06, 0.24, nzf2)
dyr = copy.deepcopy(dxr)
for iz in range(nzf2):
  dyr[iz] *= np.sqrt(2.0/3.0)
xr = []
nxr = []
yr = []
nyr = []
for iz in range(nzf2):
  xr.append(np.arange(0.0, 1.0, dxr[iz]))
  nxr.append(len(xr[iz]))
  yr.append(np.arange(0.0, 1.0, dyr[iz]))
  nyr.append(len(yr[iz]))
xrplot = []
yrplot = []
zrplot = []
srplot = []
for iz in range(nzf2):
  for iy in range(nyr[iz]):
    for ix in range(nxr[iz]):
      if iy%2 == 0:
        xrplot.append(xr[iz][ix])
      else:
        xrplot.append(xr[iz][ix]+0.5/float(nxr[iz]-1))
      yrplot.append(yr[iz][iy])
      zrplot.append(zf2[iz])
      srplot.append(sr[iz])

# NICAS sampling
fig,ax = plt.subplots(ncols=1, nrows=3, figsize=(12,12), subplot_kw={'projection': '3d'})

ax[0].view_init(elev=20, azim=25)
ax[0].scatter(xfplot1, yfplot1, zfplot1, c=zfplot1, s=0.5, marker='.', alpha=0.8, cmap='rainbow')
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].set_zticks([])
ax[0].set_xlim(0.0, 1.0)
ax[0].set_ylim(0.0, 1.0)
ax[0].set_zlim(0.0, 1.0)
ax[0].text2D(0.05, 0.8, 'a)', fontsize=20, transform=ax[0].transAxes)

ax[1].view_init(elev=20, azim=25)
ax[1].scatter(xfplot2, yfplot2, zfplot2, c=zfplot2, s=0.5, marker='.', alpha=0.8, cmap='rainbow')
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_zticks([])
ax[1].set_xlim(0.0, 1.0)
ax[1].set_ylim(0.0, 1.0)
ax[1].set_zlim(0.0, 1.0)
ax[1].text2D(0.05, 0.8, 'b)', fontsize=20, transform=ax[1].transAxes)

ax[2].view_init(elev=20, azim=25)
ax[2].scatter(xrplot, yrplot, zrplot, c=zrplot, s=srplot, marker='.', alpha=0.8, cmap='rainbow')
ax[2].set_xticks([])
ax[2].set_yticks([])
ax[2].set_zticks([])
ax[2].set_xlim(0.0, 1.0)
ax[2].set_ylim(0.0, 1.0)
ax[2].set_zlim(0.0, 1.0)
ax[2].text2D(0.05, 0.8, 'c)', fontsize=20, transform=ax[2].transAxes)

plt.subplots_adjust(hspace=-0.115)
plt.savefig('../fig/split_grid.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/split_grid.pdf', '../fig/split_grid.pdf'])
