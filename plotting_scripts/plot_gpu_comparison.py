#! /usr/bin/env python
"""Plots comparison of GPU performance for Jacobian matrix evaluations.
"""
from __future__ import print_function

import numpy as np

from performance_comparison import fullscale_comp

# Location of label: (data index, x position multiplier, y position multiplier)
text_loc = [(3, 0.85, 0.9), #fd
            (3, 0.87, 0.4), #pyjac
            ]

fit_params, data = fullscale_comp('cuda', text_loc=text_loc, loc_override=4)

for x in fit_params:
    print(x[0] + '\tR^2 : {}'.format(x[1]))

pJ = next(val for val in fit_params if 'pyJac' in val[0])
fD = next(val for val in fit_params if 'Finite' in val[0])

print('Finite difference / pyJac performance ratios: ')
for i in range(len(data[fit_params.index(fD)])):
    print(data[fit_params.index(fD)][i] / data[fit_params.index(pJ)][i])
