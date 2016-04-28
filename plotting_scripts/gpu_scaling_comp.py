#! /usr/bin/env python
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

from performance_extractor import get_data
from general_plotting import legend_key

font_size = 'large'

def plot_scaling(plotdata, markerlist, colorlist, miny, label_locs=None,
                 plot_std=True, hollow=False
                 ):
    """
    """
    mset = list(set(x.mechanism for x in plotdata))
    mechs = sorted(mset, key=lambda mech:next(x for x in plotdata
                   if x.mechanism == mech).num_specs
                   )
    for i, mech in enumerate(mechs):
        name = legend_key[mech]
        data = [x for x in plotdata if x.mechanism == mech]
        thex = sorted(list(set(x.x for x in data)))
        they = [next(x.y for x in data if x.x == xval) for xval in thex]
        thez = [np.std(x) for x in they]
        they = [np.mean(x) for x in they]
        miny = they[0] if miny is None else they[0] if they[0] < miny else miny
        argdict = {'x':thex,
                   'y':they,
                   'linestyle':'',
                   'marker':markerlist[i],
                   'markeredgecolor':colorlist[i],
                   'markersize':8,
                   'color':colorlist[i],
                   'label':name
                   }
        if hollow:
            argdict['markerfacecolor'] = 'None'
            argdict['label'] += ' (smem)'
        if plot_std:
            argdict['yerr'] = thez
            line = plt.errorbar(**argdict)
        else:
            line = plt.plot(**argdict)

        if label_locs is not None:
            # get index of first value after specified location
            label_loc, label_off = label_locs[i]
            pos_label = next(x[0] for x in enumerate(thex) if x[1] > label_loc)
            label_ypos = 0.5 * (they[pos_label] + they[pos_label - 1])
            plt.text(label_loc, label_ypos*label_off, name, fontsize=font_size,
                     horizontalalignment='center', verticalalignment='center'
                     )

    return miny

legend_markers = ['o', 'v', 's', '>']
legend_colors = ['b', 'g', 'r', 'c']

label_locs = [(10, 2.0),
              (10, 0.5),
              (10, 2.0),
              (10, 2.0)
              ]

# Get CUDA pyJac datapoints, without cache optimization or shared memory
data = get_data()
plotdata = [x for x in data if x.lang == 'cuda'
            and not x.cache_opt
            and not x.smem
            and not x.finite_difference
            ]

fig, ax = plt.subplots()
miny = None

miny = plot_scaling(plotdata, legend_markers, legend_colors, miny, label_locs)
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_ylim(ymin=miny*0.95)
#ax.legend(loc=0, numpoints=1, frameon=False)
# add some text for labels, title and axes ticks
ax.set_ylabel('Mean evaluation time', fontsize=font_size)
ax.set_xlabel('Number of conditions', fontsize=font_size)
plt.savefig('gpu_scaling.pdf')
plt.close()


# Get CUDA pyJac datapoints with shared memory
plotdata = [x for x in data if x.lang == 'cuda'
            and not x.cache_opt
            and x.smem
            and not x.finite_difference
            ]

fig, ax = plt.subplots()
miny = plot_scaling(plotdata, legend_markers, legend_colors, miny, hollow=True)

ax.set_yscale('log')
ax.set_xscale('log')
ax.set_ylim(ymin=miny*0.95)
ax.legend(loc=0, numpoints=1, frameon=False)
# add some text for labels, title and axes ticks
ax.set_ylabel('Mean evaluation time')
ax.set_xlabel('Number of conditions')
#ax.legend(loc=0)
plt.savefig('gpu_scaling_smem.pdf')
plt.close()
