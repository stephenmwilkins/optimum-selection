


import FLARE.io.sextractor as sex

import numpy as np

cat, attributes = sex.read('../../data/Yung19_lightcone.dat')


import h5py

h5 = h5py.File('../../data/Yung19_lightcone.hdf5', 'w')

for i,column in enumerate(cat.keys()):
    dset = h5.create_dataset(column, data=cat[column])
    dset.attrs['comments'] = attributes[i]

h5.flush()
