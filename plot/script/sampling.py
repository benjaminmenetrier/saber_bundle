#!/usr/bin/env python3

import argparse
import os
import sys
from sys import exit
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import subprocess
import copy

# Figures repository
os.makedirs("../fig", exist_ok=True)

# Load HDIAG map
f_map = Dataset('../data/randomization_doc_glb_2/1-1_rh2_000001.nc', 'r', format='NETCDF4')
lon_hdiag = f_map['lon'][0,:]
lat_hdiag = f_map['lat'][:,0]
rh_hdiag = f_map['air_horizontal_streamfunction'][0,:,:]/1000.0
rh_hdiag_cyclic, lon_hdiag_cyclic = add_cyclic_point(rh_hdiag, coord=lon_hdiag)
rh_hdiag_hom = copy.deepcopy(rh_hdiag)
for ix in range(len(lon_hdiag)):
  rh_hdiag_hom[:,ix] = lat_hdiag
rh_hdiag_cyclic_hom, lon_hdiag_cyclic_hom = add_cyclic_point(rh_hdiag_hom, coord=lon_hdiag)

# Load NICAS sampling
f_samp_reg = Dataset('../data/error_covariance_training_doc_glb_7/1-1_nicas_grids_local_000001-000001.nc', 'r', format='NETCDF4')
f_samp_rnd = Dataset('../data/error_covariance_training_doc_glb_8/1-1_nicas_grids_local_000001-000001.nc', 'r', format='NETCDF4')
f_samp_inh = Dataset('../data/error_covariance_training_doc_glb_9/1-1_nicas_grids_local_000001-000001.nc', 'r', format='NETCDF4')
lon_sa_reg = f_samp_reg['air_horizontal_streamfunction']['cmp_1']['lon_sa'][:]
lat_sa_reg = f_samp_reg['air_horizontal_streamfunction']['cmp_1']['lat_sa'][:]
lon_sa_rnd = f_samp_rnd['air_horizontal_streamfunction']['cmp_1']['lon_sa'][:]
lat_sa_rnd = f_samp_rnd['air_horizontal_streamfunction']['cmp_1']['lat_sa'][:]
lon_sa_inh = f_samp_inh['air_horizontal_streamfunction']['cmp_1']['lon_sa'][:]
lat_sa_inh = f_samp_inh['air_horizontal_streamfunction']['cmp_1']['lat_sa'][:]

# Resolution
resol = 7.0

# Normalization
rh_hdiag_cyclic = rh_hdiag_cyclic/resol

# Map bounds
rh_min = np.min(rh_hdiag_cyclic)
rh_max = np.max(rh_hdiag_cyclic)
levels = np.linspace(rh_min, rh_max, 100)
norm = plt.Normalize(vmin=rh_min, vmax=rh_max)
cmap = mpl.colormaps['coolwarm']
rgba = cmap(norm(3000.0/resol))

# NICAS sampling
fig,ax = plt.subplots(ncols=1, nrows=3, figsize=(6,12),subplot_kw=dict(projection=ccrs.NearsidePerspective(central_longitude=160.0, central_latitude=25.0, satellite_height=3.e7)))
ax[0].coastlines(linewidth=0.5)
ax[0].contourf(lon_hdiag_cyclic_hom, lat_hdiag, rh_hdiag_cyclic_hom, colors=rgba, transform=ccrs.PlateCarree())
ax[0].plot(lon_sa_reg, lat_sa_reg, color='k', linewidth=0, markersize=1, marker='.', transform=ccrs.PlateCarree())
ax[1].coastlines(linewidth=0.5)
ax[1].contourf(lon_hdiag_cyclic_hom, lat_hdiag, rh_hdiag_cyclic_hom, colors=rgba, transform=ccrs.PlateCarree())
ax[1].plot(lon_sa_rnd, lat_sa_rnd, color='k', linewidth=0, markersize=1, marker='.', transform=ccrs.PlateCarree())
ax[2].coastlines(linewidth=0.5)
ax[2].contourf(lon_hdiag_cyclic, lat_hdiag, rh_hdiag_cyclic, levels=levels, cmap='coolwarm', transform=ccrs.PlateCarree())
ax[2].plot(lon_sa_inh, lat_sa_inh, color='k', linewidth=0, markersize=1, marker='.', transform=ccrs.PlateCarree())
fig.tight_layout()
fig.text(0.25, 0.97, 'a)', fontsize=20.0)
fig.text(0.25, 0.6975, 'b)', fontsize=20.0)
fig.text(0.25, 0.425, 'c)', fontsize=20.0)
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, orientation='horizontal', pad=0.02, ax=ax, shrink=0.5)
plt.savefig('../fig/nicas_sampling.pdf', format='pdf', dpi=300)
plt.close()
subprocess.run(['pdfcrop', '../fig/nicas_sampling.pdf', '../fig/nicas_sampling.pdf'])
