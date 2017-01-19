Demonstrating TChem's Lack of Thread-Safety
-------------------------------------------

This directory holds a self-contained example of how TChem is not thread-safe when
parallelized with OpenMP. The testing program first uses TChem to evaluate the chemical
kinetic Jacobian for a number of thermo-chemical states in an entirely
single-threaded (i.e., serial) manner. Next, the tester turns on OpenMP parallelization
and re-computes the Jacobian matrices for the same thermo-chemical states.
Finally, the tester compares the results from the single-threaded and multi-threaded
evaluations, and determines the error relative to the single-threaded version.
In all cases tested, significant error is found for the multi-threaded version.

To run the TChem multi-threaded tester, the following are required,
and should be available on the `PATH`:
*  A Python installation with NumPy installed
*  A TChem installation, with the environment variable `TCHEM_HOME` set to the
installation directory (i.e., where `include/` and `lib/` reside). Alternatively,
line 4 of the `makefile` may be altered to direct to the correct installation path.
*  A `gcc` installation with OpenMP

Finally, to run the tester call:
```
$ python run_test.py
```

OR

```
$ ./run_test.py
```
