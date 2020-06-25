




import numpy as np

import FLARE.plt as fplt
import FLARE.photom as photo
import FLARE.surveys

import h5py
import pickle


selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W'], ['Webb.NIRCam.F115W','Webb.NIRCam.F150W','Webb.NIRCam.F200W']]

s_f = selection_filters

all_filters = []
for s in selection_filters: all_filters += s

all_filters = list(set(all_filters))
filters = all_filters

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



detection_filter = 'Webb.NIRCam.F200W'



flux_limit = SNR_detection * noise[detection_filter] # nJy in final band

# --- convert catalogue magnitudes to fluxes and place in new dictionary

fluxes = {f: photo.m_to_flux(cat[convert_filter_Y19(f)+'_dust'][:])  for f in filters} # f_nu/nJy

for f in filters:
    fluxes[f] += noise[f]*np.random.randn(N)


# --- define selection regions

N_trials = 100000

sel = np.zeros((2,4))

output = {'contamination': [], 'completeness': [], 'selection': [], 'accuracy': []}

for j in range(N_trials):

    sel[0][0] = np.random.uniform(low = 0.5, high = 1.0)
    sel[0][1] = np.random.uniform(low = -0.2, high = 0.2)
    sel[0][2] = np.random.uniform(low = 0.5, high = 1.0)
    sel[0][3] = np.random.uniform(low = 0.5, high = 2.0)

    sel[1][0] = np.random.uniform(low = 0.5, high = 1.0)
    sel[1][1] = np.random.uniform(low = -0.2, high = 0.2)
    sel[1][2] = np.random.uniform(low = 0.5, high = 1.0)
    sel[1][3] = np.random.uniform(low = 0.5, high = 2.0)



    c01 = fluxes[s_f[0][0]]/fluxes[s_f[0][1]] # break colour (mag) - usually on y-axis
    c02 = fluxes[s_f[0][-2]]/fluxes[s_f[0][-1]] # slope colour (mag) - usually on x-axis

    c11 = fluxes[s_f[1][0]]/fluxes[s_f[1][1]] # break colour (mag) - usually on y-axis
    c12 = fluxes[s_f[1][-2]]/fluxes[s_f[1][-1]] # slope colour (mag) - usually on x-axis

    detected = (fluxes[detection_filter]>flux_limit)

    s0 = (c02>sel[0][0])&(c01<sel[0][2]*(c02-sel[0][0])+sel[0][1])&(c01<sel[0][2]*(sel[0][3]-sel[0][0])+sel[0][1])
    s1 = (c12>sel[1][0])&(c11<sel[1][2]*(c12-sel[1][0])+sel[1][1])&(c11<sel[1][2]*(sel[1][3]-sel[1][0])+sel[1][1])

    s = (s0|s1)&detected

    # --- contamination and completeness

    if len(z[s]>0):

        output['selection'].append(sel)
        output['contamination'].append(len(z[(s)&(z<5)])/len(z[(s)]))
        output['completeness'].append(len(z[(s)&(z>6)])/len(z[(detected)&(z>6)]))

        print(f'{j}')


pickle.dump(output, open('optimise_joint.p','wb'))
