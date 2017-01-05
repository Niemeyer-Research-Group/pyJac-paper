"""Module with
"""
import numpy as np
import matplotlib.pyplot as plt

font_size = 'large'

legend_key = {'H2':r'H$_2$/CO',
              'CH4':r'GRI-Mech 3.0',
              'C2H4':r'USC-Mech II',
              'IC5H11OH':r'IC$_5$H$_{11}$OH'
              }

def plot(plotdata, marker, name, minx=None, miny=None, plot_std=True,
         norm=None, return_y=False, reacs_as_x=True, color=None, hollow=False
         ):
    """Plot performance as a function of reaction count.
    """
    if reacs_as_x:
        plotdata = sorted(plotdata, key=lambda x: x.num_reacs)
        x_vals = [x.num_reacs for x in plotdata]
    else:
        plotdata = sorted(plotdata, key=lambda x: x.num_specs)
        x_vals = [x.num_specs for x in plotdata]
    if norm is None:
        y_vals = [np.array(x.y) / x.x for x in plotdata]
    else:
        y_vals = [norm(x) for x in plotdata]

    err_vals = [np.std(y) for y in y_vals]
    y_vals = [np.mean(y) for y in y_vals]
    argdict = {'x':x_vals,
               'y':y_vals,
               'linestyle':'',
               'marker':marker,
               'label':name
               }
    if color:
        argdict['markeredgecolor'] = color
        argdict['color'] = color
    elif hollow:
        argdict['markerfacecolor'] = 'None'
        argdict['label'] += ' (smem)'
    if plot_std:
        argdict['yerr'] = err_vals
    if plot_std:
        line = plt.errorbar(**argdict)
    else:
        line = plt.plot(**argdict)

    minx = (x_vals[0] if minx is None
            else x_vals[0] if x_vals[0] < minx
            else minx
            )
    miny = (y_vals[0] if miny is None
            else y_vals[0] if y_vals[0] < miny
            else miny
            )
    retval = minx, miny
    if return_y:
        retval = (retval, y_vals, err_vals)
    return retval


def plot_scaling(plotdata, markerlist, colorlist, minx=None, miny=None,
                 label_locs=None, plot_std=True, hollow=False
                 ):
    """Plots performance data with varying number of conditions.
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
        minx = (np.min(x_vals) if minx is None
                else np.min(x_vals) if np.min(x_vals) < minx
                else minx
                )
        miny = (np.min(y_vals) if miny is None
                else np.min(y_vals) if np.min(y_vals) < miny
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
            del argdict['x']
            del argdict['y']
            line = plt.plot(x_vals, y_vals, **argdict)

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
