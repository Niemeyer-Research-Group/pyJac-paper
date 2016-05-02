#! /usr/bin/env python
"""Plots GPU performance scaling data for pyJac Jacobian matrix evaluation.
"""

import matplotlib.pyplot as plt
import numpy as np

# Local imports
from performance_extractor import get_data
from general_plotting import plot_scaling

font_size = 'large'

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
plt.savefig('gpu_performance_scaling.pdf')
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
plt.savefig('gpu_performance_scaling_shmem.pdf')
plt.close()
