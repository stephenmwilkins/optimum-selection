




import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import FLARE.plt as fplt
import FLARE.photom as photo
import FLARE.surveys

import h5py


cmap = mpl.cm.viridis
norm = mpl.colors.Normalize(vmin=0, vmax=10)


# --- define filters for colour-colour diagram




selection_filters = [['Webb.NIRCam.F090W', 'Webb.NIRCam.F115W','Webb.NIRCam.F150W'], ['Webb.NIRCam.F115W','Webb.NIRCam.F150W','Webb.NIRCam.F200W']]



all_filters = []
for s in selection_filters: all_filters += s


# convert FLARE filter to format to Yung19

def convert_filter_Y19(f):
    return '_'.join(f.split('.')[1:])



# --- define selection regions


selections = [(0.7, 0.0, 0.8, 1.2),(0.7, 0.0, 0.8, 1.2)]

selections = [(0.7, 1.2),(0.7, 1.2)]

# flat f_nu noise

noise = {f: 1. for f in all_filters} # nJy

noise = FLARE.surveys.surveys['Webb10k'].fields['base'].depths # nJy

print(noise)


SNR_detection = 10.


# --- read HDF5 version of the catalogue

cat = h5py.File('../../data/Aaron/Yung19_lightcone.hdf5', 'r')

# --- print number of rows

z = cat['redshift'][:]
N = len(z)


for i in range(len(selection_filters)):

    filters = selection_filters[i]

    flux_limit = SNR_detection * noise[filters[-1]] # nJy in final band

    print(f'magnitude limit: {photo.flux_to_m(flux_limit)}')

    sel = selections[i]


    for add_noise in [True, False]:

        print('-'*40)
        print(add_noise)

        if add_noise:
            label = '_wNOISE'
        else:
            label = '_woNOISE'

        # --- convert catalogue magnitudes to fluxes and place in new dictionary

        fluxes = {f: photo.m_to_flux(cat[convert_filter_Y19(f)+'_dust'][:])  for f in filters} # f_nu/nJy

        if add_noise:
            for f in filters:
                fluxes[f] += noise[f]*np.random.randn(N)




        c1 = fluxes[filters[0]]/fluxes[filters[1]] # break colour (mag) - usually on y-axis
        c2 = fluxes[filters[-2]]/fluxes[filters[-1]] # slope colour (mag) - usually on x-axis

        s_all = (fluxes[filters[-1]]>flux_limit)

        s = (c2>sel[0])&(c1<sel[2]*(c2-sel[0])+sel[1])&(c1<sel[2]*(sel[3]-sel[0])+sel[1])&s_all


        # ------------------
        # plot all objects coloured by redshift

        fig = plt.figure(figsize = (4, 4))

        left  = 0.15
        bottom = 0.15
        width = 0.7
        height = 0.7

        ax = fig.add_axes((left, bottom, width, height))
        im = ax.scatter(c2[s_all], c1[s_all], c=cmap(norm(z[s_all])), s=1)

        ax.set_xlim([-0.3, 2.0])
        ax.set_ylim([-0.3, 2.0])

        x_label = rf'$\rm f_{{\nu, { filters[-2].split(".")[2] } }} / f_{{\nu, { filters[-1].split(".")[2] } }} $'
        y_label = rf'$\rm f_{{\nu, { filters[0].split(".")[2] } }} / f_{{\nu, { filters[1].split(".")[2] } }} $'
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        z_bar_ax = fig.add_axes((left, bottom+height, width, 0.025))
        z_cbar = mpl.colorbar.ColorbarBase(z_bar_ax, cmap=cmap, norm=norm, orientation='horizontal')
        z_cbar.set_label(r'$\rm z$')
        z_bar_ax.xaxis.set_ticks_position('top')
        z_bar_ax.xaxis.set_label_position('top')


        fig.savefig(f'figures/all_{i}_{label}.png') # probaby need to use png due to so many points
        fig.clf() # clear figure




        # ------------------
        # plot selection region and objects in the selection region

        fig = plt.figure(figsize = (4, 6))

        left  = 0.15
        bottom = 0.1
        width = 0.8
        height = 0.45
        N_height = 0.15
        C_height = 0.15

        ax = fig.add_axes((left, bottom, width, height))
        N_ax = fig.add_axes((left, bottom+height+0.05, width, N_height))
        C_ax = fig.add_axes((left, bottom+height+N_height+0.05, width, C_height))

        # N_ax.get_xaxis().set_ticks([])
        C_ax.get_xaxis().set_ticks([])

        # --- contamination

        contamination = len(z[(s)&(z<5)])/len(z[(s)])
        print(f'contamination: {contamination}')

        # --- plot selection region

        x = [sel[0], sel[0], sel[3], 2]
        y = [-1, sel[1], sel[2]*(sel[3]-sel[0])+sel[1], sel[2]*(sel[3]-sel[0])+sel[1]]

        ax.fill_between(x, y, [-2]*4, color='k', alpha=0.1)



        ax.plot(x,y, color='k', lw=1)

        ax.scatter(c2[s_all], c1[s_all], c=cmap(norm(z[s_all])), s=1, alpha = 0.01, cmap = cmap) # --- plot all objects

        ax.scatter(c2[s], c1[s], c=cmap(norm(z[s])), s=1) # --- plot all objects meeting the selection

        ax.set_xlim([-0.3, 2.0])
        ax.set_ylim([-0.3, 2.0])

        x_label = rf'$\rm f_{{\nu, { filters[-2].split(".")[2] } }} / f_{{\nu, { filters[-1].split(".")[2] } }} $'
        y_label = rf'$\rm f_{{\nu, { filters[0].split(".")[2] } }} / f_{{\nu, { filters[1].split(".")[2] } }} $'
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)


        # --- add N

        binw = 0.1
        bins = np.arange(0, 10, binw)
        Ngal, bin_edges = np.histogram(z[s], bins=bins)
        bin_centres = bin_edges + binw/2.

        N_ax.plot(bin_centres[:-1], Ngal/binw, c='0.5', lw=1)

        N_ax.set_xlim([0, 10.])
        N_ax.set_ylabel(r'$\rm N\ dz$')

        # --- add N


        N_all, bin_edges = np.histogram(z[s_all], bins=bins)
        C = Ngal/N_all

        C_ax.plot(bin_centres[:-1], C, c='0.5', lw=1)

        C_ax.set_xlim([0, 10.])
        C_ax.set_ylim([0, 1.1])
        C_ax.set_ylabel(r'$\rm C$')


        # --- add colorbar

        z_bar_ax = fig.add_axes((left, bottom+height+N_height+C_height + 0.05, width, 0.025))
        z_cbar = mpl.colorbar.ColorbarBase(z_bar_ax, cmap=cmap, norm=norm, orientation='horizontal')
        z_cbar.set_label(r'$\rm z$')
        z_bar_ax.xaxis.set_ticks_position('top')
        z_bar_ax.xaxis.set_label_position('top')

        fig.savefig(f'figures/selection_{i}_{label}.png')
        fig.clf()
