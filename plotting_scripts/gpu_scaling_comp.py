#! /usr/bin/env python
"""Plots GPU performance data for pyJac Jacobian matrix evaluation.
"""

import matplotlib.pyplot as plt
import numpy as np

# Local imports
from performance_extractor import get_data
from general_plotting import legend_key

font_size = 'large'

def plot_scaling(plotdata, markerlist, colorlist, minx=None, miny=None,
                 label_locs=None, plot_std=True, hollow=False
                 ):
    """Plots performance data for multiple mechanisms.
    """
    mset = list(set(x.mechanism for x in plotdata))
    mechs = sorted(mset, key=lambda mech:next(x for x in plotdata
                   if x.mechanism == mech).num_specs
                   )
    for i, mech in enumerate(mechs):
        name = legend_key[mech]
        data = [x for x in plotdata if x.mechanism == mech]
        x_vals = sorted(list(set(x.x for x in data)))
        y_vals = [next(x.y for x in data if x.x == xval) for xval in x_vals]
        y_vals = [np.mean(x) for x in y_vals]
        err_vals = [np.std(x) for x in y_vals]

        # Find minimum x and y values, or keep manual setting if actually
        # lower than true minimums
        minx = (x_vals[0] if minx is None
                else x_vals[0] if x_vals[0] < minx
                else minx
                )
        miny = (y_vals[0] if miny is None
                else y_vals[0] if y_vals[0] < miny
                else miny
                )

        argdict = {'x':x_vals,
                   'y':y_vals,
                   'linestyle':'',
                   'marker':markerlist[i],
                   'markeredgecolor':colorlist[i],
                   'markersize':8,
                   'color':colorlist[i],
                   'label':name
                   }
        # use hollow symbols for shared memory results
        if hollow:
            argdict['markerfacecolor'] = 'None'
            argdict['label'] += ' (smem)'
        # plotting error bars for standard deviation
        if plot_std:
            argdict['yerr'] = err_vals
            line = plt.errorbar(**argdict)
        else:
            line = plt.plot(**argdict)

        # Rather than legend, place labels above/below series
        if label_locs is not None:
            # get index of first value after specified location
            label_loc, label_off = label_locs[i]
            pos_label = next(x[0] for x in enumerate(x_vals) if x[1] > label_loc)
            # average of points
            label_ypos = 0.5 * (y_vals[pos_label] + y_vals[pos_label - 1])
            plt.text(label_loc, label_ypos*label_off, argdict['label'],
                     fontsize=font_size,
                     horizontalalignment='center', verticalalignment='center'
                     )

    return minx, miny

legend_markers = ['o', 'v', 's', '>']
legend_colors = ['b', 'g', 'r', 'c']

# x position of text label, and multiplier for y position
label_locs = [(10, 1.75),
              (10, 0.6),
              (10, 1.75),
              (10, 1.75)
              ]

# Get CUDA pyJac datapoints, without cache optimization or shared memory
data = get_data()
plotdata = [x for x in data if x.lang == 'cuda'
            and not x.cache_opt
            and not x.smem
            and not x.finite_difference
            ]

fig, ax = plt.subplots()
minx, miny = plot_scaling(plotdata, legend_markers, legend_colors,
                          label_locs=label_locs
                          )
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_ylim(ymin=miny*0.85)
ax.set_xlim(xmin=minx*0.85)
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
minx, miny = plot_scaling(plotdata, legend_markers, legend_colors,
                          label_locs=label_locs, hollow=True
                          )

ax.set_yscale('log')
ax.set_xscale('log')
ax.set_ylim(ymin=miny*0.85)
ax.set_xlim(xmin=minx*0.85)
#ax.legend(loc=0, numpoints=1, frameon=False)
# add some text for labels, title and axes ticks
ax.set_ylabel('Mean evaluation time', fontsize=font_size)
ax.set_xlabel('Number of conditions', fontsize=font_size)
plt.savefig('gpu_scaling_smem.pdf')
plt.close()
