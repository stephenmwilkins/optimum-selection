


import numpy as np

import FLARE
cosmo = FLARE.default_cosmo()
import FLARE.SED.models as models
import FLARE.plt as fplt
import FLARE.photom as photo
import FLARE.surveys
import FLARE.filters

import h5py




h5 = h5py.File('../../data/beta.hdf5', 'w')


filters = FLARE.surveys.surveys['Webb10k'].fields['base'].filters
lamz = np.arange(1000, 30000, 1) # observed frame wavelength
F = FLARE.filters.add_filters(filters, new_lam = lamz)

Ndim = 100

N = Ndim**2

h5.create_dataset('z', data = np.random.uniform(low=5, high=12, size=N))
h5.create_dataset('beta', data = np.random.uniform(low=-3, high=2, size=N))
# h5.create_dataset('beta', data = -2.*np.ones(N))

for f in filters:
    h5.create_dataset(f, data = np.zeros(N))

for i, (z, beta) in enumerate(zip(h5['z'][:], h5['beta'][:])):



    lam = lamz/(1+z)

    m = models.beta(lam, beta, 1)

    m.get_fnu(cosmo, z)
    fluxes = m.return_Fnu(F)

    for f in filters:
        h5[f][i] = fluxes[f]

    print(i, z, 1E28*fluxes['Webb.NIRCam.F090W'], 1E28*fluxes['Webb.NIRCam.F115W'], 1E28*fluxes['Webb.NIRCam.F150W'])

h5.flush()
