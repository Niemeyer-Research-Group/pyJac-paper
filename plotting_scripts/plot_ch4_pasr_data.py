#! /usr/bin/env python
"""Plots partially stirred reactor results for methane-air.
"""
import sys
import os.path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

font_size = 'large'

home_dir = os.path.join(sys.path[0], '../')
home_dir = os.path.realpath(home_dir)
fig_dir = os.path.join(home_dir, 'figures')

# Load CH4/air, 600 K results
state_data = np.load(os.path.join(home_dir, 'data', 'CH4', 'pasr_out_ch4_1.npy'))

# First plot the mean temperature
times = state_data[:, 0, 0]
mean_temp = np.zeros(state_data.shape[0])
for i in range(len(mean_temp)):
    mean_temp[i] = np.mean(state_data[i, :, 1])

plt.plot(times, mean_temp)
plt.xlim([0, 0.05])
plt.ylim([1900, 2400])
plt.xlabel('Time (s)', fontsize=font_size)
plt.ylabel('Mean temperature (K)', fontsize=font_size)

pp = PdfPages(os.path.join(fig_dir, 'CH4_600K_1atm_mean_temperature.pdf'))
pp.savefig()
pp.close()

plt.close()

# Now plot particle data
state_data = state_data.reshape(state_data.shape[0] * state_data.shape[1],
                                state_data.shape[2]
                                )


# Time vs temperature

plt.subplot(211)
plt.scatter(state_data[:,1], state_data[:,0], s=10, marker='.', c='k')
plt.ylabel('Time (s)', fontsize=font_size)
plt.xlim([600, 2400])
plt.ylim([0, 0.05])

plt.subplot(212)
n, bins, patches = plt.hist(state_data[:,1], 100,
                            normed=1, histtype='stepfilled'
                            )
plt.ylabel('PDF', fontsize=font_size)
plt.xlabel('Temperature (K)', fontsize=font_size)

pp = PdfPages(os.path.join(fig_dir, 'CH4_600K_1atm_particle_temperature.pdf'))
pp.savefig()
pp.close()
