




import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import FLARE
cosmo = FLARE.default_cosmo()
import FLARE.SED.models as models
import FLARE.plt as fplt
import FLARE.photom as photo
import FLARE.surveys
import FLARE.filters
import FLARE.plt as fplt

import h5py


cmap = mpl.cm.magma
# norm = mpl.colors.Normalize(vmin=0, vmax=10)
#

# --- define filters for colour-colour diagram


selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W'], ['Webb.NIRCam.F115W','Webb.NIRCam.F150W','Webb.NIRCam.F200W']]

# selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W']]

all_filters = []
for s in selection_filters: all_filters += s


all_filters = list(set(all_filters))




# --- define selection regions

selections = [(0.7, 0.0, 0.8, 1.2),(0.7, 0.0, 0.8, 1.2)]

# flat f_nu noise

noise = {f: 1. for f in all_filters} # nJy

noise = FLARE.surveys.surveys['Webb10k'].fields['base'].depths # nJy

print(noise)

noise = {key:value for key,value in noise.items()}


SNR_detection = 100.



cat = h5py.File('../../data/beta_lum.hdf5', 'r') # contains only \beta, z, and fluxes




# fig = plt.figure()

# left  = 0.15
# bottom = 0.15
# width = 0.8
# height = 0.8
#
# ax = fig.add_axes((left, bottom, width, height))
# ax.set_facecolor('0.0')

fig, axes = plt.subplots(1, 2, sharey=True, figsize = (4, 2))
fig.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.95, wspace=0, hspace=0)

for i, ax in zip(range(len(selection_filters)), axes):


    filters = selection_filters[i]

    flux_limit = SNR_detection * noise[filters[-1]] # nJy in final band

    print(f'magnitude limit: {photo.flux_to_m(flux_limit)}')

    sel = selections[i]

    N = len(cat['z'][:])

    fluxes = {f: cat[f][:]  for f in filters} # f_nu/nJy
    for f in filters:
        fluxes[f] += noise[f]*np.random.randn(N)

    c1 = fluxes[filters[0]]/fluxes[filters[1]] # break colour (mag) - usually on y-axis
    c2 = fluxes[filters[-2]]/fluxes[filters[-1]] # slope colour (mag) - usually on x-axis

    s_all = (fluxes[filters[-1]]>flux_limit)

    s = (c2>sel[0])&(c1<sel[2]*(c2-sel[0])+sel[1])&(c1<sel[2]*(sel[3]-sel[0])+sel[1])&s_all



    ranges = [[6, 11.99], [-3, 1]]
    bins = [20,20]

    H_detected, xedges, yedges = np.histogram2d(cat['z'][s_all], cat['beta'][s_all], bins=bins, range=ranges)
    H_selected, xedges, yedges = np.histogram2d(cat['z'][s], cat['beta'][s], bins=bins, range=ranges)
    H_all, xedges, yedges = np.histogram2d(cat['z'][:], cat['beta'][:], bins=bins, range=ranges)


    R = H_selected.T/H_all.T

    ax.imshow(R, extent = [*ranges[0], *ranges[1]], origin='lower', cmap = cmap, aspect = 'auto', alpha = 1.0)

    ax.set_xlabel(r'$\rm z$')

axes[0].set_ylabel(r'$\rm \beta$')


fig.savefig(f'figures/beta.pdf')
fig.clf()






fig = plt.figure(figsize = (3, 3))

left  = 0.2
bottom = 0.2
width = 0.75
height = 0.75

ax = fig.add_axes((left, bottom, width, height))

H_detected = {}
H_selected = {}

for i in range(len(selection_filters)):

    filters = selection_filters[i]

    flux_limit = SNR_detection * noise[filters[-1]] # nJy in final band

    print(f'magnitude limit: {photo.flux_to_m(flux_limit)}')

    sel = selections[i]

    N = len(cat['z'][:])

    fluxes = {f: cat[f][:]  for f in filters} # f_nu/nJy
    for f in filters:
        fluxes[f] += noise[f]*np.random.randn(N)

    c1 = fluxes[filters[0]]/fluxes[filters[1]] # break colour (mag) - usually on y-axis
    c2 = fluxes[filters[-2]]/fluxes[filters[-1]] # slope colour (mag) - usually on x-axis

    s_all = (fluxes[filters[-1]]>flux_limit)

    s = (c2>sel[0])&(c1<sel[2]*(c2-sel[0])+sel[1])&(c1<sel[2]*(sel[3]-sel[0])+sel[1])&s_all



    ranges = [[6, 11.99], [-3, 1]]
    bins = [20,20]

    H_detected[i], xedges, yedges = np.histogram2d(cat['z'][s_all], cat['beta'][s_all], bins=bins, range=ranges)
    H_selected[i], xedges, yedges = np.histogram2d(cat['z'][s], cat['beta'][s], bins=bins, range=ranges)
    H_all, xedges, yedges = np.histogram2d(cat['z'][:], cat['beta'][:], bins=bins, range=ranges)



R = (H_selected[0]+H_selected[1])/H_all
# R = (H_detected[0]+H_detected[1])/H_all

ax.imshow(R.T, extent = [*ranges[0], *ranges[1]], origin='lower', cmap = cmap, aspect = 'auto', alpha = 1.0)

ax.set_xlabel(r'$\rm z$')
ax.set_ylabel(r'$\rm \beta$')


fig.savefig(f'figures/beta_joint.pdf')
fig.clf()
