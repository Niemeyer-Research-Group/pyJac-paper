pyJac: analytical Jacobian generator for chemical kinetics
==========================================================

This repository contains the source for our paper describing an analytical Jacobian generator for chemical kinetic models.
It makes use of the [`pyJac`](http://github.com/kyleniemeyer/pyjac/) package, which has been developed concurrently.
To see a current build of the paper from the master branch of this repository, refer to http://kyleniemeyer.github.io/pyJac-paper/ (powered by [gh-publisher](https://github.com/ewanmellor/gh-publisher) and inspired by the [multiband_LS repository](http://jakevdp.github.io/multiband_LS)).

Feel free to submit comments or feedback via the Issues tab on this repository.

Reproducing the Paper
---------------------
The LaTeX source of the paper is in the top directory.

To reproduce all of the figures in the paper, first install packages from the standard Python scientific stack: [numpy](http://numpy.org), [scipy](http://scipy.org), and [matplotlib](http://matplotlib.org).
Then, from the top directory, the five figures in the paper can be generated using our data by:

```
$ python plotting_scripts/plot_cpu_comparison.py
$ python plotting_scripts/plot_gpu_scaling.py
$ python plotting_scripts/plot_gpu_comparison.py
$ python plotting_scripts/plot_ch4_pasr_data.py
```


License
-------
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
