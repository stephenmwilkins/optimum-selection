




import numpy as np

import FLARE.plt as fplt
import FLARE.photom as photo
import FLARE.surveys

import h5py
import pickle


selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W'], ['Webb.NIRCam.F115W','Webb.NIRCam.F150W','Webb.NIRCam.F200W']]

selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W']]


all_filters = []
for s in selection_filters: all_filters += s


# convert FLARE filter to format to Yung19

def convert_filter_Y19(f):
    return '_'.join(f.split('.')[1:])




# --- DEFINE NOISE



# noise = {f: 1. for f in all_filters} # nJy # --- flat f_nu noise
noise = FLARE.surveys.surveys['Webb10k'].fields['base'].depths # nJy # --- default noise

SNR_detection = 10.

# --- read HDF5 version of the catalogue

cat = h5py.File('../../data/Aaron/Yung19_lightcone.hdf5', 'r')

# --- print number of rows

z = cat['redshift'][:]
N = len(z)


selections = [(0.7, 0.0, 0.8, 1.2),(0.7, 0.0, 0.8, 1.2)]

for i in range(len(selection_filters)):


    filters = selection_filters[i]

    flux_limit = SNR_detection * noise[filters[-1]] # nJy in final band

    # --- convert catalogue magnitudes to fluxes and place in new dictionary

    fluxes = {f: photo.m_to_flux(cat[convert_filter_Y19(f)+'_dust'][:])  for f in filters} # f_nu/nJy

    for f in filters:
        fluxes[f] += noise[f]*np.random.randn(N)


    # --- define selection regions

    N_trials = 10000


    sel = np.zeros(4)

    output = {'contamination': [], 'completeness': [], 'selection': []'}

    for j in range(N_trials):

        sel[0] = np.random.uniform(low = 0.5, high = 1.0)
        sel[1] = np.random.uniform(low = -0.2, high = 0.2)
        sel[2] = np.random.uniform(low = 0.5, high = 1.0)
        sel[3] = np.random.uniform(low = 0.5, high = 2.0)


        c1 = fluxes[filters[0]]/fluxes[filters[1]] # break colour (mag) - usually on y-axis
        c2 = fluxes[filters[-2]]/fluxes[filters[-1]] # slope colour (mag) - usually on x-axis

        s_all = (fluxes[filters[-1]]>flux_limit)

        s = (c2>sel[0])&(c1<sel[2]*(c2-sel[0])+sel[1])&(c1<sel[2]*(sel[3]-sel[0])+sel[1])&s_all

        # --- contamination and completeness

        if len(z[s]>0):

            output['selection'].append(sel)
            output['contamination'].append(len(z[(s)&(z<5)])/len(z[(s)]))
            output['completeness'].append(len(z[(s)&(z>6)])/len(z[(s_all)&(z>6)]))

            print(f'{j}')


pickle.dump(output, open('optimise_single.p','wb'))
