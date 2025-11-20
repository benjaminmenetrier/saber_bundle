#!/usr/bin/env python3

import os
import sys
from sys import exit
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import numpy as np
import subprocess

# Datasets
data_c0 = Dataset('../data/error_covariance_training_doc_glb_4/1-1_dirac_nicas.nc', 'r', format='NETCDF4')
data_c1 = Dataset('../data/error_covariance_training_doc_glb_5/1-1_dirac_nicas.nc', 'r', format='NETCDF4')
data_si = Dataset('../data/error_covariance_training_doc_glb_6/1-1_dirac_nicas.nc', 'r', format='NETCDF4')

# Domain
ixc = 200
dxc = 40
iyc = 100
dyc = 40

# Load data
lon = data_c0['lon'][iyc-dyc:iyc+dyc+1,ixc-dxc:ixc+dxc+1]-180.0
lat = data_c0['lat'][iyc-dyc:iyc+dyc+1,ixc-dxc:ixc+dxc+1]
phi_c0 = data_c0['air_horizontal_streamfunction'][0,iyc-dyc:iyc+dyc+1,ixc-dxc:ixc+dxc+1]
phi_c1 = data_c1['air_horizontal_streamfunction'][0,iyc-dyc:iyc+dyc+1,ixc-dxc:ixc+dxc+1]
phi_si = data_si['air_horizontal_streamfunction'][0,iyc-dyc:iyc+dyc+1,ixc-dxc:ixc+dxc+1]

# Load extended data
lat_ext = data_c0['lat'][iyc-dyc-1:iyc+dyc+2,ixc-dxc:ixc+dxc+1]
phi_c0_ext = data_c0['air_horizontal_streamfunction'][0,iyc-dyc-1:iyc+dyc+2,ixc-dxc:ixc+dxc+1]
phi_c1_ext = data_c1['air_horizontal_streamfunction'][0,iyc-dyc-1:iyc+dyc+2,ixc-dxc:ixc+dxc+1]
phi_si_ext = data_si['air_horizontal_streamfunction'][0,iyc-dyc-1:iyc+dyc+2,ixc-dxc:ixc+dxc+1]

# Compute u
u_c0 = np.zeros((2*dyc+1, 2*dxc+1))
u_c1 = np.zeros((2*dyc+1, 2*dxc+1))
u_si = np.zeros((2*dyc+1, 2*dxc+1))
for iy in range(2*dyc+1):
  for ix in range(2*dxc):
    u_c0[iy,ix] = -1.0/6371229.0*(phi_c0_ext[iy+2,ix]-phi_c0_ext[iy,ix])/(lat_ext[iy+2,ix]-lat_ext[iy,ix])
    u_c1[iy,ix] = -1.0/6371229.0*(phi_c1_ext[iy+2,ix]-phi_c1_ext[iy,ix])/(lat_ext[iy+2,ix]-lat_ext[iy,ix])
    u_si[iy,ix] = -1.0/6371229.0*(phi_si_ext[iy+2,ix]-phi_si_ext[iy,ix])/(lat_ext[iy+2,ix]-lat_ext[iy,ix])

# Dirac levels
levels_phi = np.linspace(-0.01, 1.0, 11)
umax = max([np.max(np.abs(u_c0)),np.max(np.abs(u_c1)),np.max(np.abs(u_si))])
levels_u = np.linspace(-umax, umax, 21)

# Figure
fig,ax = plt.subplots(ncols=3,nrows=2, figsize=(12,8))
ax[0][0].set_title("C0 interpolation", fontsize=16)
ax[0][0].set_ylabel("Stream function", fontsize=16)
ax[0][0].contourf(lon, lat, phi_c0, levels=levels_phi, cmap='viridis_r')
ax[0][0].contour(lon, lat, phi_c0, levels=levels_phi, colors='k')
ax[0][0].contour(lon, lat, phi_c0, levels=levels_phi, colors='k')
ax[0][0].plot(lon[dyc,dxc], lat[dyc,dxc], "k", linewidth=0, markersize=6, marker='o')
ax[0][0].set_xticks([])
ax[0][0].set_yticks([])
ax[0][1].set_title("C1 interpolation", fontsize=16)
ax[0][1].contourf(lon, lat, phi_c1, levels=levels_phi, cmap='viridis_r')
ax[0][1].contour(lon, lat, phi_c1, levels=levels_phi, colors='k')
ax[0][1].plot(lon[dyc,dxc], lat[dyc,dxc], "k", linewidth=0, markersize=6, marker='o')
ax[0][1].set_xticks([])
ax[0][1].set_yticks([])
ax[0][2].set_title("Smoothing interpolation", fontsize=16)
ax[0][2].contourf(lon, lat, phi_si, levels=levels_phi, cmap='viridis_r')
ax[0][2].contour(lon, lat, phi_si, levels=levels_phi, colors='k')
ax[0][2].plot(lon[dyc,dxc], lat[dyc,dxc], "k", linewidth=0, markersize=6, marker='o')
ax[0][2].set_xticks([])
ax[0][2].set_yticks([])
ax[1][0].set_ylabel("Eastward wind", fontsize=16)
ax[1][0].contourf(lon, lat, u_c0, levels=levels_u, cmap='coolwarm')
ax[1][0].contour(lon, lat, u_c0, levels=levels_u, colors='k')
ax[1][0].plot(lon[dyc,dxc], lat[dyc,dxc], "k", linewidth=0, markersize=6, marker='o')
ax[1][0].set_xticks([])
ax[1][0].set_yticks([])
ax[1][1].contourf(lon, lat, u_c1, levels=levels_u, cmap='coolwarm')
ax[1][1].contour(lon, lat, u_c1, levels=levels_u, colors='k')
ax[1][1].plot(lon[dyc,dxc], lat[dyc,dxc], "k", linewidth=0, markersize=6, marker='o')
ax[1][1].set_xticks([])
ax[1][1].set_yticks([])
ax[1][2].contourf(lon, lat, u_si, levels=levels_u, cmap='coolwarm')
ax[1][2].contour(lon, lat, u_si, levels=levels_u, colors='k')
ax[1][2].plot(lon[dyc,dxc], lat[dyc,dxc], "k", linewidth=0, markersize=6, marker='o')
ax[1][2].set_xticks([])
ax[1][2].set_yticks([])
plt.savefig('../fig/interpolation.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/interpolation.pdf', '../fig/interpolation.pdf'])
