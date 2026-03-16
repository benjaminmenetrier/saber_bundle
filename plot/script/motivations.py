#!/usr/bin/env python3

import os
import matplotlib.pylab as plt
import numpy as np
import subprocess

# Figures repository
os.makedirs("../fig", exist_ok=True)

# Define full grid
dxf = 0.025
dyf = dxf*np.sqrt(2.0/3.0)
xf = np.arange(0.0, 1.0, dxf)
yf = np.arange(0.0, 1.0, dyf)
nxf = len(xf)
nyf = len(yf)
xfplot = []
yfplot = []
for iy in range(nyf):
  for ix in range(nxf):
    if iy%2 == 0:
      xfplot.append(xf[ix])
    else:
      xfplot.append(xf[ix]+0.5/float(nxf-1))
    yfplot.append(yf[iy])

# Define reduced grid
dxr = 0.09
dyr = dxr*np.sqrt(2.0/3.0)
xr = np.arange(0.0, 1.0, dxr)
yr = np.arange(0.0, 1.0, dyr)
nxr = len(xr)
nyr = len(yr)
xrplot = []
yrplot = []
for iy in range(nyr):
  for ix in range(nxr):
    if iy%2 == 0:
      xrplot.append(xr[ix])
    else:
      xrplot.append(xr[ix]+0.5/float(nxr-1))
    yrplot.append(yr[iy])

# NICAS sampling
fig,ax = plt.subplots(ncols=1, nrows=2, figsize=(6,12))
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r"""\usepackage{bm}"""
ax[0].plot(xfplot, yfplot, color='k', linewidth=0, markersize=3, marker='.', zorder=0)
i = int(29.45*nxf)
xcf = xfplot[i]
ycf = yfplot[i]
for i in range(nxf*nyf):
  d = np.sqrt((xfplot[i]-xcf)**2+(yfplot[i]-ycf)**2)
  if d <= 0.3:
    ax[0].plot(xfplot[i], yfplot[i], color='r', linewidth=0, markersize=6, marker='.', zorder=0)
ax[0].add_artist(plt.Circle((xcf,ycf), 0.3, fill=False))
ax[0].text(0.544, 0.69, r'$\bm{r}$', fontsize=30, color='b', backgroundcolor="w", zorder=0)
ax[0].plot(xcf, ycf, color='b', markersize=15, marker='.', zorder=0)
ax[0].quiver(xcf, ycf, np.cos(0.5), np.sin(0.5), color='b', scale_units="inches", scale=0.58, zorder=1)
i = int(18.46*nxf)
ax[0].plot([xfplot[i], xfplot[i+1]], [yfplot[i], yfplot[i+1]], color='r', linewidth=2, markersize=6, marker='.', zorder=0)
ax[0].text(0.44, 0.4, r"$\bm{\gamma}$", fontsize=30, color='r', backgroundcolor="w")
ax[0].set_aspect('equal', adjustable='box') 
ax[0].set_xlim([0.25*dxf,1.0-0.25*dxf])
ax[0].set_ylim([0.25*dyf,1.0-0.25*dyf])
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].text(0.02, 0.93, 'a)', fontsize=30, backgroundcolor="w")

ax[1].plot(xrplot, yrplot, color='k', linewidth=0, markersize=6, marker='.', zorder=0)
i = int(8.45*nxr)
xcr = xrplot[i]
ycr = yrplot[i]
for i in range(nxr*nyr):
  d = np.sqrt((xrplot[i]-xcr)**2+(yrplot[i]-ycr)**2)
  if d <= 0.3:
    ax[1].plot(xrplot[i], yrplot[i], color='r', linewidth=0, markersize=12, marker='.', zorder=0)
ax[1].add_artist(plt.Circle((xcr,ycr), 0.3, fill=False))
ax[1].text(0.54, 0.69, r'$\bm{r}$', fontsize=30, color='b', backgroundcolor="w", zorder=0)
ax[1].plot(xcr, ycr, color='b', markersize=18, marker='.', zorder=0)
ax[1].quiver(xcr, ycr, np.cos(0.5), np.sin(0.5), color='b', scale_units="inches", scale=0.58, zorder=1)
i = int(5.4*nxr)
ax[1].plot([xrplot[i], xrplot[i+1]], [yrplot[i], yrplot[i+1]], color='r', linewidth=2, markersize=12, marker='.', zorder=0)
ax[1].text(0.43, 0.4, r'$\bm{\widehat{\gamma}}$', fontsize=30, color='r', backgroundcolor="w")
ax[1].set_aspect('equal', adjustable='box') 
ax[1].set_xlim([0.25*dxf,1.0-0.25*dxf])
ax[1].set_ylim([0.25*dyf,1.0-0.25*dyf])
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].text(0.02, 0.93, 'b)', fontsize=30, backgroundcolor="w")
fig.tight_layout()
plt.savefig('../fig/motivations.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/motivations.pdf', '../fig/motivations.pdf'])
