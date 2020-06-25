




import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import FLARE.plt as fplt
import FLARE.photom as photo
import FLARE.surveys
import h5py

selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W'], ['Webb.NIRCam.F115W','Webb.NIRCam.F150W','Webb.NIRCam.F200W']]

def convert_filter_Y19(f):
    return '_'.join(f.split('.')[1:])

# --- define selection regions

selections = [(0.7, 0.0, 0.8, 1.2),(0.7, 0.0, 0.8, 1.2)]



# noise = {f: 1. for f in all_filters} # nJy # --- flat f_nu noise
noise = FLARE.surveys.surveys['Webb10k'].fields['base'].depths # nJy # --- default noise

SNR_detection = 10.


# --- read HDF5 version of the catalogue

cat = h5py.File('../../data/Aaron/Yung19_lightcone.hdf5', 'r')

# --- print number of rows

z = cat['redshift'][:]
N = len(z)



# --- figure

fig = plt.figure(figsize = (4, 3))

left  = 0.15
bottom = 0.15
width = 0.8
height = 0.4

ax_N = fig.add_axes((left, bottom, width, height))
ax_C = fig.add_axes((left, bottom+height, width, height))



for i in range(len(selection_filters)):

    print('-'*40, i)

    filters = selection_filters[i]

    flux_limit = SNR_detection * noise[filters[-1]] # nJy in final band

    print(f'magnitude limit: {photo.flux_to_m(flux_limit)}')

    sel = selections[i]


    fluxes = {f: photo.m_to_flux(cat[convert_filter_Y19(f)+'_dust'][:])  for f in filters} # f_nu/nJy

    for f in filters:
        fluxes[f] += noise[f]*np.random.randn(N)

    c1 = fluxes[filters[0]]/fluxes[filters[1]] # break colour (mag) - usually on y-axis
    c2 = fluxes[filters[-2]]/fluxes[filters[-1]] # slope colour (mag) - usually on x-axis

    s_all = (fluxes[filters[-1]]>flux_limit)

    s = (c2>sel[0])&(c1<sel[2]*(c2-sel[0])+sel[1])&(c1<sel[2]*(sel[3]-sel[0])+sel[1])&s_all


    # --- contamination

    contamination = len(z[(s)&(z<5)])/len(z[(s)])
    print(f'contamination: {contamination}')

    # --- add Number

    binw = 0.1
    bins = np.arange(0, 10, binw)
    Ngal, bin_edges = np.histogram(z[s], bins=bins)
    bin_centres = bin_edges + binw/2.

    ax_N.plot(bin_centres[:-1], Ngal/binw, c='0.5', lw=1)


    # --- add Completeness

    N_all, bin_edges = np.histogram(z[s_all], bins=bins)
    C = Ngal/N_all

    ax_C.plot(bin_centres[:-1], C, c='0.5', lw=1)






ax_N.set_xlim([0, 10.])
ax_N.set_ylabel(r'$\rm N\ dz$')

ax_C.set_xlim([0, 10.])
ax_C.set_ylim([0, 1.1])
ax_C.set_ylabel(r'$\rm C$')

fig.savefig(f'figures/combined.pdf')
fig.clf()
