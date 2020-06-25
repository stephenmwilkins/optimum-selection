
# plot histogram of log10(flux)




import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import FLARE.plt as fplt
import FLARE.photom as photo
import h5py


# --- read HDF5 version of the catalogue

f = h5py.File('../../data/Yung19_lightcone.hdf5', 'r')

# --- print all columns

for k in f.keys(): print(k)

# --- print number of rows


z = f['redshift'][:]

filter = 'NIRCam_F090W'
mag = f[filter][:]
flux = photo.m_to_flux(mag)


fig = plt.figure(figsize = (4, 3))

left  = 0.15
bottom = 0.15
width = 0.8
height = 0.8

ax = fig.add_axes((left, bottom, width, height))

ax.hist(np.log10(flux), bins = np.linspace(0,6,60))

ax.set_xlabel('f_{'+filter+'}')
ax.set_ylabel('N')

fig.savefig('figures/flux_hist.pdf')
