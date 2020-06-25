




import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import FLARE.plt as fplt
import FLARE.photom as photo
import h5py


# --- define filters for colour-colour diagram

c1_filters = ['NIRCam_F090W', 'NIRCam_F115W'] # break colour filters
c2_filters = ['NIRCam_F115W', 'NIRCam_F150W'] # slope colour
filters = list(set(c1_filters+c2_filters))

# --- define selection region

selection = (1.5, 0.5, 1, 2)  # break limit, slope start, slope slope, slope limit

noise = {'NIRCam_F090W': 10., 'NIRCam_F115W': 10., 'NIRCam_F150W': 10.} # nJy

SNR_detection = 10.

flux_limit = SNR_detection * noise[c2_filters[1]] # nJy in final band

add_noise = True






# --- read HDF5 version of the catalogue

cat = h5py.File('../../data/Yung19_lightcone.hdf5', 'r')

# --- print all columns

for k in cat.keys(): print(k)

# --- print number of rows


z = cat['redshift'][:]

N = len(z)




for add_noise in [True, False]:


    if add_noise:
        label = '_wNOISE'
    else:
        label = '_woNOISE'

    # --- convert catalogue magnitudes to fluxes and place in new dictionary

    fluxes = {f: photo.m_to_flux(cat[f+'_dust'][:])  for f in filters} # f_nu/nJy

    if add_noise:
        for f in filters:
            fluxes[f] += noise[f]*np.random.randn(N)



    c1 = -2.5*np.log10(fluxes[c1_filters[0]]/fluxes[c1_filters[1]]) # break colour (mag) - usually on y-axis
    c2 = -2.5*np.log10(fluxes[c2_filters[0]]/fluxes[c2_filters[1]]) # slope colour (mag) - usually on x-axis

    s_all = (fluxes[c2_filters[1]]>flux_limit)

    s = (c1>selection[0])&(c1>selection[2]*(c2-selection[1])+selection[0])&(c2<selection[3])&(fluxes[c2_filters[1]]>flux_limit)




    # ------------------
    # plot all objects coloured by redshift

    fig = plt.figure(figsize = (4, 4))

    left  = 0.15
    bottom = 0.15
    width = 0.8
    height = 0.8

    ax = fig.add_axes((left, bottom, width, height))
    im = ax.scatter(c2[s_all], c1[s_all], c=z[s_all], s=1)
    fig.colorbar(im, ax=ax)
    ax.set_xlabel('-'.join(c2_filters))
    ax.set_ylabel('-'.join(c1_filters))
    fig.savefig(f'figures/cc_all{label}.png') # probaby need to use png due to so many points
    fig.clf() # clear figure




    # ------------------
    # plot selection region and objects in the selection region

    fig = plt.figure(figsize = (4, 4))

    left  = 0.15
    bottom = 0.15
    width = 0.8
    height = 0.8


    ax = fig.add_axes((left, bottom, width, height))

    # --- plot selection region

    ax.plot([-5, selection[1], selection[3], selection[3]], [selection[0], selection[0], selection[0] + selection[2]*(selection[3]-selection[1]), 10])

    ax.scatter(c2, c1, c='k', s=1, alpha = 0.01) # --- plot all objects
    ax.scatter(c2[s], c1[s], c=z[s], s=1) # --- plot all objects meeting the selection

    ax.set_xlabel('-'.join(c2_filters))
    ax.set_ylabel('-'.join(c1_filters))



    fig.savefig(f'figures/cc_selection{label}.png')

    # --- plot redshift histogram region


    fig = plt.figure(figsize = (4, 3))

    left  = 0.15
    bottom = 0.15
    width = 0.8
    height = 0.8

    ax = fig.add_axes((left, bottom, width, height))

    bins = np.linspace(0,10,100)

    # ax.hist(z, bins=bins, color='0.8')
    ax.hist(z[s], bins=bins, color='0.3')

    ax.set_xlabel('z')
    ax.set_ylabel('N')



    fig.savefig(f'figures/cc_selection_z{label}.pdf')
