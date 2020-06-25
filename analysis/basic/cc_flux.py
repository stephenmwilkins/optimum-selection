




import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import FLARE.plt as fplt
import FLARE.photom as photo
import h5py


cmap = mpl.cm.viridis
norm = mpl.colors.Normalize(vmin=0, vmax=10)


# --- define filters for colour-colour diagram

c1_filters = ['NIRCam_F090W', 'NIRCam_F115W'] # break colour filters
c2_filters = ['NIRCam_F115W', 'NIRCam_F150W'] # slope colour


c1_filters = ['NIRCam_F115W', 'NIRCam_F150W']
c2_filters = ['NIRCam_F150W', 'NIRCam_F200W']

filters = list(set(c1_filters+c2_filters))

# --- define selection region

selection = (0.7, 0.0, 0.8, 1.2)  # break limit, slope start, slope slope, slope limit
sel = selection

n = 1.

noise = {'NIRCam_F090W': n, 'NIRCam_F115W': n, 'NIRCam_F150W': n, 'NIRCam_F200W': n} # nJy

SNR_detection = 10.



flux_limit = SNR_detection * noise[c2_filters[1]] # nJy in final band

print(f'magnitude limit: {photo.flux_to_m(flux_limit)}')

add_noise = True






# --- read HDF5 version of the catalogue

cat = h5py.File('../../data/Yung19_lightcone.hdf5', 'r')

# --- print number of rows


z = cat['redshift'][:]

N = len(z)




for add_noise in [True, False]:

    print('-'*40)
    print(add_noise)

    if add_noise:
        label = '_wNOISE'
    else:
        label = '_woNOISE'

    # --- convert catalogue magnitudes to fluxes and place in new dictionary

    fluxes = {f: photo.m_to_flux(cat[f+'_dust'][:])  for f in filters} # f_nu/nJy

    if add_noise:
        for f in filters:
            fluxes[f] += noise[f]*np.random.randn(N)



    c1 = fluxes[c1_filters[0]]/fluxes[c1_filters[1]] # break colour (mag) - usually on y-axis
    c2 = fluxes[c2_filters[0]]/fluxes[c2_filters[1]] # slope colour (mag) - usually on x-axis

    s_all = (fluxes[c2_filters[1]]>flux_limit)

    s = (c2>sel[0])&(c1<selection[2]*(c2-selection[0])+selection[1])&(c1<selection[2]*(sel[3]-selection[0])+selection[1])&s_all


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

    x_label = rf'$\rm f_{{\nu, { c2_filters[0].split("_")[1] } }} / f_{{\nu, { c2_filters[1].split("_")[1] } }} $'
    y_label = rf'$\rm f_{{\nu, { c1_filters[0].split("_")[1] } }} / f_{{\nu, { c1_filters[1].split("_")[1] } }} $'
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    z_bar_ax = fig.add_axes((left, bottom+height, width, 0.025))
    z_cbar = mpl.colorbar.ColorbarBase(z_bar_ax, cmap=cmap, norm=norm, orientation='horizontal')
    z_cbar.set_label(r'$\rm z$')
    z_bar_ax.xaxis.set_ticks_position('top')
    z_bar_ax.xaxis.set_label_position('top')


    fig.savefig(f'figures/cc_flux_all{label}.png') # probaby need to use png due to so many points
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

    x_label = rf'$\rm f_{{\nu, { c2_filters[0].split("_")[1] } }} / f_{{\nu, { c2_filters[1].split("_")[1] } }} $'
    y_label = rf'$\rm f_{{\nu, { c1_filters[0].split("_")[1] } }} / f_{{\nu, { c1_filters[1].split("_")[1] } }} $'
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


    # --- add N

    binw = 0.1
    bins = np.arange(0, 10, binw)
    N, bin_edges = np.histogram(z[s], bins=bins)
    bin_centres = bin_edges + binw/2.

    N_ax.plot(bin_centres[:-1], N/binw, c='0.5', lw=1)

    N_ax.set_xlim([0, 10.])
    N_ax.set_ylabel(r'$\rm N\ dz$')

    # --- add N


    N_all, bin_edges = np.histogram(z[s_all], bins=bins)
    C = N/N_all

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

    fig.savefig(f'figures/cc_flux_selection{label}.png')
    fig.clf()
