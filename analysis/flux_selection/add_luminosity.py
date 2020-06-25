




import numpy as np
import FLARE.surveys
import h5py

cat = h5py.File('../../data/beta.hdf5', 'r') # contains only \beta, z, and fluxes

filters = FLARE.surveys.surveys['Webb10k'].fields['base'].filters

h5 = h5py.File('../../data/beta_lum.hdf5', 'w')


Ndim = 100


h5.create_dataset('z', data = np.repeat(cat['z'][:], Ndim))
h5.create_dataset('beta', data = np.repeat(cat['beta'][:], Ndim))
h5.create_dataset('log10_luminosity', data = np.random.uniform(low=27, high=31, size=Ndim**3))

for f in filters:

    data = 10**h5['log10_luminosity'][:]*np.repeat(cat[f][:], Ndim)
    h5.create_dataset(f, data = data)


h5.flush()
