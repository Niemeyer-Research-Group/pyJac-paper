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
import copy

home_dir = None
font_size = 'large'

legend_markers = ['o', 'v', 's', '>']
legend_colors = ['b', 'g', 'r', 'c']

# x position of text label, and multiplier for y position
label_locs = [(16, 2.2),
              (16, 0.75),
              (16, 2.2),
              (16, 2.2)
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
    #ax.set_xscale('log')
    ax.set_ylim(ymin=miny*0.85)
    ax.set_xlim(xmin=minx*0.85, xmax=35)
    #ax.legend(loc=0, numpoints=1, frameon=False)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mean evaluation time per condition (ms)', fontsize=font_size)
    ax.set_xlabel('Number of CPU threads', fontsize=font_size)
    pp = PdfPages(os.path.join(d, outname))
    pp.savefig()
    pp.close()
    plt.close()

    #num of cores on cpu
    cutoff = 40
    scalings = []
    #draw scaling lines
    for mech in set(x.mechanism for x in plotdata):
        per_mech = [x for x in plotdata if x.mechanism == mech
                    and x.x <= cutoff
                    ]
        per_mech = sorted(per_mech, key=lambda x: x.x)
        eff = [np.mean(per_mech[0].y) / (per_mech[i].x * np.mean(per_mech[i].y))
               for i in range(len(per_mech))
               ]
        eff_x = [per_mech[i].x for i in range(len(per_mech))]
        per_mech = [copy.copy(pd) for pd in per_mech[:]]
        for i in range(len(per_mech)):
            per_mech[i].x = eff_x[i]
            per_mech[i].y = eff[i]
        scalings.extend(per_mech)

    fig, ax = plt.subplots()
    minx, miny = plot_scaling(scalings, legend_markers, legend_colors, plot_std=False)
    #ax.legend(loc=0)
    #ax.set_xscale('log')
    ax.set_ylim(ymin=miny*0.98, ymax=1.02)
    ax.set_xlim(xmin=0, xmax=35)

    ax.legend(loc=0, numpoints=1, fontsize=font_size,
              shadow=True, fancybox=True
              )
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Parallel scaling efficiency', fontsize=font_size)
    ax.set_xlabel('Number of CPU threads', fontsize=font_size)
    ind = outname.index('.pdf')
    outname = outname[:ind] + '_par' + '.pdf'
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
