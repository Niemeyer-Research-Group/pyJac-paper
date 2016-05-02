"""Module for extracting Jacobian matrix eval performance data.
"""

# Standard library
import sys
import os
import os.path
import json

import numpy as np

def parse_file(directory, mech, filename, num_specs, num_reacs):
    data_arr = []
    with open(os.path.join(directory, filename)) as file:
        lines = [line.strip() for line in file.readlines()]
    data = {}
    for line in lines:
        try:
            x1, y1 = [float(f) for f in line.split(',')]
            if not x1 in data:
                data[x1] = []
            data[x1].append(y1)
        except:
            assert line == 'SUCCESS'
            pass
    for x in data:
        data_arr.append(data_point(mech, filename, num_specs,
                        num_reacs, x, data[x])
                        )
    return data_arr


class data_point(object):
    def __init__(self, mechanism, filename, num_specs, num_reacs, x, y):
        self.mechanism = mechanism

        lang, cache_opt, smem, fd, dummy = filename.split('_')
        self.lang = lang
        self.cache_opt = cache_opt == 'co'
        self.smem = smem == 'smem'
        self.finite_difference = fd == 'fd'

        self.num_specs = num_specs
        self.num_reacs = num_reacs
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "lang={},\tmech={},\tFD={},\tsmem={}\tco={}\n".format(
            self.lang, self.mechanism, self.finite_difference,
            self.smem, self.cache_opt
            )


def get_data(home_dir=None):
    if home_dir is None:
        home_dir = os.path.join(sys.path[0], '../')
        home_dir = os.path.realpath(home_dir)
    d = os.path.join(home_dir, 'performance')
    dirs = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

    #ok, now we have a list of data directories, open each and look for the text files
    data = []
    for directory in dirs:
        thedir = os.path.join(d, directory)

        #get text files with performance data
        files = [o for o in os.listdir(thedir) if
                 os.path.isfile(os.path.join(thedir,o)) and o.endswith('.txt')
                 ]

        # read mechanism info
        mech_meta_file = next(s for s in os.listdir(thedir) if s.endswith('.json'))
        with open(os.path.join(d, directory, mech_meta_file), 'r') as f:
            mech_info = json.load(f)

        for filename in files:
            data.extend(parse_file(thedir, directory, filename,
                                   mech_info['num_species'],
                                   mech_info['num_reactions']
                                   )
                        )
    return data
