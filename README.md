pyJac: analytical Jacobian generator for chemical kinetics
==========================================================

This repository contains the source for our paper describing an analytical Jacobian generator for chemical kinetic models.
It makes use of the [`pyJac`](https://github.com/SLACKHA/pyJac) package, which has been developed concurrently. The paper was published in *Computer Physics Communications*:

 > Kyle E. Niemeyer, Nicholas J. Curtis, and Chih-Jen Sung. 2017. "pyJac: analytical Jacobian generator for chemical kinetics." Computer Physics Communications, 215:188–203. https://doi.org/10.1016/j.cpc.2017.02.004

and a preprint is available at [`arXiv:1605.03262 [physics.comp-ph]`](http://arxiv.org/abs/1605.03262).

All of the data, plotting scripts, and figures associated with the paper can be found on Figshare:

 > Niemeyer, Kyle; Curtis, Nick; Sung, Chih-Jen (2017): Data, plotting scripts, and figures for "pyJac: analytical Jacobian generator for chemical kinetics". figshare. https://doi.org/10.6084/m9.figshare.4578010.v1

To see a current build of the paper from the master branch of this repository, refer to https://niemeyer-research-group.github.io/pyJac-paper/ (powered by [gh-publisher](https://github.com/ewanmellor/gh-publisher) and inspired by the [multiband_LS repository](http://jakevdp.github.io/multiband_LS)).

Feel free to submit comments or feedback via the Issues tab on this repository.


Reproducing the Paper
---------------------
The LaTeX source of the paper is in the top directory.

To reproduce all of the figures in the paper, first install packages from the standard Python scientific stack: [numpy](http://numpy.org), [scipy](http://scipy.org), and [matplotlib](http://matplotlib.org).
Then, from the top directory, the five figures in the paper can be generated using our data by:

```bash
$ python plotting_scripts/plot_cpu_comparison.py
$ python plotting_scripts/plot_gpu_scaling.py
$ python plotting_scripts/plot_gpu_comparison.py
$ python plotting_scripts/plot_cpu_scaling.py
$ python plotting_scripts/plot_ch4_pasr_data.py
```

The underlying data can be reproduced by installing the pyjac package, available multiple ways:

1. The easiest way is to install via [`conda`](https://conda.io/):
```bash
$ conda install -c slackha pyjac
```

2. You can also install using `pip`:
```bash
$ pip install pyjac
```

3. If neither of the previous methods are available, you can also download the source code from GitHub (https://github.com/SLACKHA/pyJac) and install using `setuptools`:
```bash
$ wget https://github.com/SLACKHA/pyJac/archive/master.zip
$ unzip master.zip
$ cd pyJac-master
$ python setup.py install
```

Then, all of the functional and performance test results can be reproduced (albeit on different systems for the latter, which will alter values) by using the model and PaSR input files given in the data repository mentioned above (https://doi.org/10.6084/m9.figshare.4578010.v1).


Demonstrating TChem's Lack of Thread-Safety
-------------------------------------------
The folder `tchem_multithread_test/` holds a self-contained example demonstrating
TChem's lack of thread safety. See `tchem_multithread_test/README.md` for more details.


License
-------
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
See the LICENSE.txt file or follow the link for details.
