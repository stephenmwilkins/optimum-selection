




import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm




# ------------------
# plot selection region and objects in the selection region

fig = plt.figure(figsize = (4, 4))

left  = 0.15
bottom = 0.15
width = 0.8
height = 0.8


ax = fig.add_axes((left, bottom, width, height))

x = np.arange(-1,5,0.01)

# y = (-0.1/(x-1.0))+0.5

y = 0.5 - np.exp(-4*(x-0.5))

ax.plot(x,y, color='k', lw=1)


y = 0.5 + np.exp(4*(x-0.5))

ax.plot(x,y, color='k', lw=1)



ax.set_xlim([-0.3, 2.0])
ax.set_ylim([-0.3, 2.0])



fig.savefig(f'figures/simple.pdf')
fig.clf()
