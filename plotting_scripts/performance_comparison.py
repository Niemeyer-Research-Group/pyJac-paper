"""Module for performance comparison plotting.
"""
from __future__ import print_function

# Standard library
import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import optimize

# Local imports
from performance_extractor import get_data
from general_plotting import legend_key, plot

font_size = 'large'

FD_marker = '>'
pj_marker = 'o'
tc_marker = 's'

def fr_exp10(x):
    """Returns base 10 mantissa and exponent of float.
    """
    # ensure number
    assert isinstance(x, (int, float))
    exp = int(np.log10(x))
    mantissa = x / 10**exp
    if mantissa < 1.0:
        mantissa *= 10.
        exp -= 1
    return mantissa, exp


def nice_names(x):
    """Returns data series names for printing.
    """
    if x.finite_difference:
        name = 'Finite Difference'
        marker = FD_marker
    elif x.lang == 'tchem':
        name = 'TChem'
        marker = tc_marker
    else:
        name = 'pyJac'
        marker = pj_marker
    if x.lang == 'cuda':
        name += ' (GPU)'
    return name, marker


def get_fullscale(data):
    mechanisms = set([x.mechanism for x in data])
    #need to filter out runs on subsets
    for mech in mechanisms:
        max_x = max(x.x for x in [y for y in data if y.mechanism == mech])
        data = [x for x in data if x.mechanism != mech or
                (x.x == max_x)
                ]
    return data


def fit_order(plotdata, y_vals, std, order=None, color='k', text_loc=None):
    """Gets and plots best-fit line for performance data.
    """
    x_vals = sorted([x.num_reacs for x in plotdata])
    maxx = int(x_vals[-1])

    def fit_func(p, x):
        n = order
        const = p[0]
        if order is None:
            n = p[0]
            const = p[1]

        # Need to handle when arguments of log may be >= 0
        if const > 0.0:
            return n * np.log10(np.array(x).clip(min=1.e-20)) + np.log10(const)
        else:
            return np.inf

    def errfunc(p, x, y):
        return (fit_func(p, x) - np.log10(y)) # Distance to the target function

    # use specified order of polynomial; otherwise, fit should find this
    if order is None:
        p0 = [1, 1] # Initial guess for the parameters
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x_vals, y_vals))
        order = p1[0]
        const = p1[1]
    else:
        p0 = [1] # Initial guess for the parameters
        p1, success = optimize.leastsq(errfunc, p0[:], args=(x_vals, y_vals))
        const = p1[0]

    # calculate r squared value of fit
    fi = const * x_vals ** order
    ss_res = np.sum(np.abs(y_vals - fi)**2)
    ss_tot = np.sum(np.abs(y_vals - np.mean(y_vals))**2)
    r_squared = 1.0 - ss_res / ss_tot

    name = nice_names(plotdata[0])[0]

    # only print fit labels if location specified
    if text_loc is not None:
        point, xoffset, yoffset = text_loc
        xbase = x_vals[point] * xoffset
        ybase = y_vals[point] * yoffset

        m, e = fr_exp10(const)
        label = r'${{{:.1f}}}$'.format(m)
        if e != 0:
            label += r'$\times 10^{{{:}}}$'.format(e)
        if order == 1:
            label += r'$N_R$'
        else:
            label += r'$N_R^{{{:.2}}}$'.format(order)

        plt.text(xbase, ybase, label, fontsize=font_size,
                 horizontalalignment='center', verticalalignment='center'
                 )

    # print to screen either way
    print(name + ' best-fit line: {:.2e} * N_R^{:.2}'.format(const, order))

    plt.plot(range(maxx + 1), const * np.array(range(maxx + 1))**order,
             'k-', color=color
             )

    return name, r_squared, const, order


def fullscale_comp(lang, plot_std=True, homedir=None,
                   cache_opt_default=False,
                   smem_default=False,
                   loc_override=None,
                   text_loc=None,
                   color_list=['b', 'g', 'r', 'k']
                   ):
    if lang == 'c':
        langs = ['c', 'tchem']
        desc = 'cpu'
        smem_default = False
    elif lang == 'cuda':
        langs = ['cuda']
        desc = 'gpu'
    else:
        raise Exception('unknown lang {}'.format(lang))

    def thefilter(x):
        return (x.cache_opt==cache_opt_default and
                x.smem == smem_default and
                x.lang in langs
                )

    fit_vals = []
    data = get_data(homedir)
    data = [x for x in data if thefilter(x)]
    data = get_fullscale(data)
    if lang == 'c':
        #ensure we take only numthreads = 1
        data = [x for x in data if x.num_threads==1]
    if not len(data):
        print('no data found... exiting')
        sys.exit(-1)

    fig, ax = plt.subplots()

    linestyle = ''

    fitvals = []
    retdata = []
    color_ind = 0
    text_ind = None
    if text_loc:
        text_ind = 0

    # finite difference
    plotdata = [x for x in data if x.finite_difference]
    if plotdata:
        color = color_list[color_ind]
        color_ind += 1
        (minx, miny), y_vals, err_vals = plot(plotdata, FD_marker,
                                              'Finite Difference',
                                              return_y=True, color=color
                                              )
        theloc = None
        if text_ind is not None:
            theloc = text_loc[text_ind]
            text_ind += 1
        fitvals.append(
            fit_order(plotdata, y_vals, err_vals, color=color, text_loc=theloc)
            )
        retdata.append(y_vals)

    for lang in langs:
        plotdata = [x for x in data if not x.finite_difference
                    and x.lang == lang
                    ]
        color = color_list[color_ind]
        color_ind += 1
        if plotdata:
            name, marker = nice_names(plotdata[0])
            (minx, miny), y_vals, err_vals = plot(plotdata, marker, name,
                                                  minx, miny,
                                                  return_y=True, color=color
                                                  )
            theloc = None
            if text_ind is not None:
                theloc = text_loc[text_ind]
                text_ind += 1
            fitvals.append(
                fit_order(plotdata, y_vals, err_vals, None, color, text_loc=theloc)
                )
            retdata.append(y_vals)

    ax.set_yscale('log')
    ax.set_ylim(ymin=miny*0.85)
    ax.set_xlim(xmin=0)
    loc = 0 if loc_override is None else loc_override
    ax.legend(loc=loc, numpoints=1, fontsize=font_size,
              #shadow=True, fancybox=True
              )
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mean evaluation time / condition (ms)', fontsize=font_size)
    ax.set_xlabel('Number of Reactions', fontsize=font_size)

    if homedir is None:
        homedir = os.path.join(sys.path[0], '../')
        homedir = os.path.realpath(homedir)
    d = os.path.join(homedir, 'figures')

    pp = PdfPages(os.path.join(d, '{}_performance_comparison.pdf'.format(desc)))
    pp.savefig()
    pp.close()

    plt.close()

    return fitvals, retdata
