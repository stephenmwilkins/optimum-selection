




import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import FLARE.plt as fplt
import h5py


# --- read HDF5 version of the catalogue

f = h5py.File('../../data/Yung19_lightcone.hdf5', 'r')

# --- print all columns

for k in f.keys(): print(k)

# --- print number of rows

z = f['redshift'][:]

# --- print number galaxies in the catalogue in total

print(len(z))

# --- print number galaxies in the catalogue above redshift limits

print(len(z[z>6]))
print(len(z[z>8]))


fig = plt.figure(figsize = (4, 3))

left  = 0.15
bottom = 0.15
width = 0.8
height = 0.8

ax = fig.add_axes((left, bottom, width, height))

ax.hist(z)

ax.set_xlabel('z')
ax.set_ylabel('N')

fig.savefig('figures/z_hist.pdf')
