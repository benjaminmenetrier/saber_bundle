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
import numpy.ma as ma
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import subprocess

# Figures repository
os.makedirs("../fig", exist_ok=True)

# Bounds
steps_min = 0.0
steps_max = 1.1

# Extent
delta = 15.0
lon_min = -78.0-delta
lon_max = -78.0+delta
lat_min = 11.6-delta
lat_max = 11.6+delta

for case in ['nicas_iso', 'nicas_ani', 'nicas_iso_lr', 'nicas_mask']:
  if case == 'nicas_iso':
    # Load NICAS steps (isotropic)
    f_steps = Dataset('../data/error_covariance_training_doc_lam_1/1-1_nicas_steps_local_000001-000001.nc', 'r', format='NETCDF4')
    steps = f_steps['air_horizontal_streamfunction']['cmp_1']

  if case == 'nicas_ani':
    # Load NICAS steps (anisotropic)
    f_steps = Dataset('../data/error_covariance_training_doc_lam_2/1-1_nicas_steps_local_000001-000001.nc', 'r', format='NETCDF4')
    steps = f_steps['air_horizontal_streamfunction']['cmp_1']

  if case == 'nicas_iso_lr':
    # Load NICAS steps (isotropic - low resolution)
    f_steps = Dataset('../data/error_covariance_training_doc_lam_3/1-1_nicas_steps_local_000001-000001.nc', 'r', format='NETCDF4')
    steps = f_steps['air_horizontal_streamfunction']['cmp_1']

  if case == 'nicas_mask':
    # Load NICAS steps (mask)
    f_steps = Dataset('../data/error_covariance_training_doc_lam_4/1-1_nicas_steps_local_000001-000001.nc', 'r', format='NETCDF4')
    steps = f_steps['air_horizontal_streamfunction']['cmp_1']

  # Plot
  fig,ax = plt.subplots(ncols=3, nrows=2, figsize=(12,6),subplot_kw=dict(projection=ccrs.LambertConformal(central_longitude=-78.0, central_latitude=11.6, standard_parallels=(11.6,11.6))))
  row = 0
  col = 0
  for i in [1,2,3,5,6,7]:
    step = steps['steps_' + str(i)]
    lon_step = step['lon'][:]
    lat_step = step['lat'][:]
    values_step = step['values'][:]
    vmax = np.max(values_step)
    ax[row][col].set_extent([lon_min,lon_max,lat_min,lat_max], ccrs.PlateCarree())
    lon_missing = []
    lat_missing = []
    values_missing = []
    for j in range(0, len(lon_step)):
      if str(type(values_step[j])) == "<class 'numpy.ma.core.MaskedConstant'>":
        lon_missing.append(lon_step[j])
        lat_missing.append(lat_step[j])
        values_missing.append(values_step[j])
    if i==1 or i==2 or i==6 or i==7:
      s = 1
    else:
      s = 4
    norm = mpl.colors.Normalize(vmin=steps_min, vmax=steps_max, clip=True)
    ax[row][col].scatter(lon_step, lat_step, s=s, c=values_step, norm=norm, cmap='viridis_r', transform=ccrs.PlateCarree())
    ax[row][col].scatter(lon_missing, lat_missing, s=s, c="lightgray", transform=ccrs.PlateCarree())
    ax[row][col].text(-79.2, -2.7, r'Maximum value: ' + str(float(f'{vmax:.2f}')), fontsize=10, transform=ccrs.PlateCarree())
    col += 1
    if col == 3:
      col = 0
      row += 1
  ax[0][0].text(-94.2, 24.5, 'a)', fontsize=12, transform=ccrs.PlateCarree())
  ax[0][1].text(-94.2, 24.5, 'b)', fontsize=12, transform=ccrs.PlateCarree())
  ax[0][2].text(-94.2, 24.5, 'c)', fontsize=12, transform=ccrs.PlateCarree())
  ax[1][0].text(-94.2, 24.5, 'd)', fontsize=12, transform=ccrs.PlateCarree())
  ax[1][1].text(-94.2, 24.5, 'e)', fontsize=12, transform=ccrs.PlateCarree())
  ax[1][2].text(-94.2, 24.5, 'f)', fontsize=12, transform=ccrs.PlateCarree())
  fig.tight_layout()
  cmap = mpl.colormaps['viridis_r']
  sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=steps_min, vmax=steps_max))
  sm.set_array([])
  plt.colorbar(sm, orientation='vertical', pad=0.02, ax=ax, shrink=1.0)
  plt.savefig('../fig/' + case + '_steps.pdf', format='pdf', dpi=300)
  plt.close()
  subprocess.run(['pdfcrop', '../fig/' + case + '_steps.pdf', '../fig/' + case + '_steps.pdf'])
