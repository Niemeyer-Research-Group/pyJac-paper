#! /usr/bin/env python
"""Plots CPU performance scaling data for pyJac Jacobian matrix evaluation.
"""

import sys
import os.path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Local imports
from performance_extractor import get_data
from general_plotting import plot_scaling

home_dir = None
font_size = 'large'

legend_markers = ['o', 'v', 's', '>']
legend_colors = ['b', 'g', 'r', 'c']

# x position of text label, and multiplier for y position
label_locs = [(10, 1.8),
              (10, 0.45),
              (10, 1.85),
              (10, 1.8)
              ]


if home_dir is None:
    home_dir = os.path.join(sys.path[0], '../')
    home_dir = os.path.realpath(home_dir)
d = os.path.join(home_dir, 'figures')


def __plot(plotdata, outname):
    fig, ax = plt.subplots()

    #convert to evaluation time / condition
    #and # of threads
    for pd in plotdata:
      pd.y = [y / pd.x for y in pd.y]
      pd.x = pd.num_threads

    minx, miny = plot_scaling(plotdata, legend_markers, legend_colors,
                              label_locs=label_locs
                              )
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim(ymin=miny*0.85)
    ax.set_xlim(xmin=minx*0.85)
    #ax.legend(loc=0, numpoints=1, frameon=False)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mean evaluation time per condition (ms)', fontsize=font_size)
    ax.set_xlabel('Number of CPU threads', fontsize=font_size)
    #set to base 2
    #ax.set_xscale('log', basex=2)
    #ax.set_yscale('log', basey=2)

    pp = PdfPages(os.path.join(d, outname))
    pp.savefig()
    pp.close()
    plt.close()


# Get C pyJac datapoints, without cache optimization or shared memory
# and varying #'s of threads'
data = get_data()
plotdata = [x for x in data if x.lang == 'c'
            and not x.cache_opt
            and not x.smem
            and not x.finite_difference
            and x.num_threads is not None
            ]
__plot(plotdata, 'cpu_performance_scaling.pdf')

plotdata = [x for x in data if x.lang == 'c'
            and not x.cache_opt
            and not x.smem
            and x.finite_difference
            and x.num_threads is not None
            ]
__plot(plotdata, 'cpu_performance_fd_scaling.pdf')

plotdata = [x for x in data if x.lang == 'tchem'
            and not x.cache_opt
            and not x.smem
            and not x.finite_difference
            and x.num_threads is not None
            ]
__plot(plotdata, 'cpu_performance_tc_scaling.pdf')
