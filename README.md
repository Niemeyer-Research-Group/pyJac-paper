pyJac: analytical Jacobian generator for chemical kinetics
==========================================================

This repository contains the source for our paper describing an analytical Jacobian generator for chemical kinetic models.
It makes use of the [`pyJac`](http://github.com/kyleniemeyer/pyjac/) package, which has been developed concurrently. The paper has been submitted to *Computer Physics Communication*, and a preprint is available at [`arXiv:1605.03262 [physics.comp-ph]`](http://arxiv.org/abs/1605.03262).

To see a current build of the paper from the master branch of this repository, refer to http://kyleniemeyer.github.io/pyJac-paper/ (powered by [gh-publisher](https://github.com/ewanmellor/gh-publisher) and inspired by the [multiband_LS repository](http://jakevdp.github.io/multiband_LS)).

This paper has now

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

Demonstrating TChem's Lack of Thread-Safety
-------------------------------------------
The folder `tchem_multithread_test/` is a self-contained example of how TChem is not self-consistent when parallelized with OpenMP.  The testing program first uses TChem to evaluate the chemical kinetic Jacobian for a number of thermo-chemical states in an entirely single-threaded manner.  Next, the tester turns on OpenMP parallelization and re-computes the Jacobians for the same thermo-chemical states.  Finally the tester compares the results from the single-threaded and multi-threaded evaluations, and determines the error relative to the single-threaded version.  In all cases tested, significant error is found for the multi-threaded version.

To run the TChem multi-threaded tester, a python installation with numpy installed is necessary along with a working version of gcc and OpenMP.  Additionally, an environment variable TCHEM_HOME should be set to the installation directory of TChem (i.e. where `include/` and `lib/` reside).  Alternately, line 4 of the makefile may be altered to direct to the correct installation path.

Finally, to run the tester, simply call:
```
$ python run_test.py
```

OR
```
$ ./run_test.py
```

License
-------
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
See the LICENSE.txt file or follow the link for details.
