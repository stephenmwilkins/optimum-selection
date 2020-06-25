




import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import pickle




d = pickle.load(open('optimise_single.p','rb'))




fig = plt.figure(figsize = (3, 3))

left  = 0.2
bottom = 0.2
width = 0.75
height = 0.75

ax = fig.add_axes((left, bottom, width, height))

ax.scatter(d['completeness'], d['contamination'], s=1, alpha=0.2)

ax.set_xlabel(r'$\rm completeness$')
ax.set_ylabel(r'$\rm contamination$')


fig.savefig(f'figures/optimise_single.pdf')
fig.clf()
