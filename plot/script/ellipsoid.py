#!/usr/bin/env python3

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import subprocess

# Define domain
nx = 1001
ny = 301
x = np.linspace(0.0, 10.0, nx)
y = np.linspace(0.0, 3.0, ny)
z = np.zeros((ny, nx))
iy = int(3*ny/5)

# Convolution function
def gc99(d):
  if (np.abs(d) < 0.5):
    out = 1-8*d**5+8*d**4+5*d**3-20/3*d**2
  elif d < 1.0:
    out = 8/3*d**5-8*d**4+5*d**3+20/3*d**2-10*d+4-1/(3*d)
  else:
    out = 0.0
  return out

# Isotropic tensor
ix1 = int(nx/6)
Dxx = 1.0**2
Dyy = 1.0**2
Dxy = 0.0
det = Dxx*Dyy-Dxy**2
Hxx = Dyy/det
Hyy = Dxx/det
Hxy = -Dxy/det
for jx in range(nx):
  dx = x[jx]-x[ix1]
  for jy in range(ny):
    dy = y[jy]-y[iy]
    d = np.sqrt(Hxx*dx**2+Hyy*dy**2+Hxy*dx*dy)
    z[jy,jx] += gc99(d)
D1 = (r"\begin{eqnarray*} \mathbf{D} = \left(\begin{array}{cc}" + str(float(f'{Dxx:.2f}')) + r" & 0 \\ 0 & " + str(float(f'{Dyy:.2f}')) + r"\end{array} \right)\end{eqnarray*}")

# Anisotropic diagonal tensor
ix2 = int(nx/2)
Dxx = 1.5**2
Dyy = 1.0**2
Dxy = 0.0
det = Dxx*Dyy-Dxy**2
Hxx = Dyy/det
Hyy = Dxx/det
Hxy = -Dxy/det
for jx in range(nx):
  dx = x[jx]-x[ix2]
  for jy in range(ny):
    dy = y[jy]-y[iy]
    d = np.sqrt(Hxx*dx**2+Hyy*dy**2+Hxy*dx*dy)
    z[jy,jx] += gc99(d)
D2 = (r"\begin{eqnarray*} \mathbf{D} = \left(\begin{array}{cc}" + str(float(f'{Dxx:.2f}')) + r" & 0 \\ 0 & " + str(float(f'{Dyy:.2f}')) + r"\end{array} \right)\end{eqnarray*}")

# Anisotropic tensor
ix3 = int(5*nx/6)
Dxx = 2.0**2
Dyy = 1.5**2
Dxy = 0.8*np.sqrt(Dxx*Dyy)
det = Dxx*Dyy-Dxy**2
Hxx = Dyy/det
Hyy = Dxx/det
Hxy = -Dxy/det
for jx in range(nx):
  dx = x[jx]-x[ix3]
  for jy in range(ny):
    dy = y[jy]-y[iy]
    d = np.sqrt(Hxx*dx**2+Hyy*dy**2+Hxy*dx*dy)
    z[jy,jx] += gc99(d)
D3 = (r"\begin{eqnarray*} \mathbf{D} = \left(\begin{array}{cc}" + str(float(f'{Dxx:.3f}')) + r" & " + str(float(f'{Dxy:.3f}')) + r" \\" + str(float(f'{Dxy:.3f}')) + r" & " + str(float(f'{Dyy:.3f}')) + r"\end{array} \right)\end{eqnarray*}")

# Plot
os.makedirs("../fig", exist_ok=True)
levels = np.linspace(0.0, 1.0, 15)
plt.rcParams['text.usetex'] = True
plt.contourf(x, y, z, levels=levels, cmap='viridis_r')
ax = plt.gca()
ax.set_aspect('equal', adjustable='box') 
ax.text(x[ix1], 0.4, D1, fontsize=10, horizontalalignment='center', verticalalignment='center')
ax.text(x[ix2], 0.4, D2, fontsize=10, horizontalalignment='center', verticalalignment='center')
ax.text(x[ix3], 0.4, D3, fontsize=10, horizontalalignment='center', verticalalignment='center')
plt.savefig('../fig/ellipsoid.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/ellipsoid.pdf', '../fig/ellipsoid.pdf'])
