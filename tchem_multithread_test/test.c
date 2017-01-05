#include <stdio.h>
#include "header.h"
#include <string.h>
#include <math.h>
#include "TC_interface.h"

void read_initial_conditions(const char* filename, int NUM, double** y_host, double** variable_host);

int main(int argc, char *argv[])
{

  char mechfile[100] = "h2.dat";
  char thermofile[100] = "h2therm.dat";

  int num_odes = 100100;
  omp_set_num_threads(1);

  double* y_host;
  double* var_host;

  read_initial_conditions("data.bin", num_odes, &y_host, &var_host);

  /* Initialize TC library */
  int withtab = 0;
  TC_initChem( mechfile, thermofile, withtab, 1.0);

  /* create saved jacobians */
  double* save_jac = (double*)calloc(NSP * NSP * num_odes, sizeof(double));

  for(int tid = 0; tid < num_odes; ++tid)
  {
      double jac[NSP * NSP] = {0};
      TC_setThermoPres(var_host[tid]) ;
      TC_getJacTYNm1anl ( &y_host[tid * NN], NSP, jac ) ;
      //save jacobian
      memcpy(&save_jac[tid * NSP * NSP], jac, NSP * NSP * sizeof(double));
  }

  //now re-run with multiple threads
  omp_set_num_threads(10);
  double* save_jac_multithread = (double*)calloc(NSP * NSP * num_odes, sizeof(double));
  #pragma omp parallel for
  for(int tid = 0; tid < num_odes; ++tid)
  {
      double jac[NSP * NSP] = {0};
      TC_setThermoPres(var_host[tid]) ;
      TC_getJacTYNm1anl ( &y_host[tid * NN], NSP, jac ) ;
      //save jacobian
      memcpy(&save_jac_multithread[tid * NSP * NSP], jac, NSP * NSP * sizeof(double));
  }

  //compute max error
  double max_err = -1;
  double max_err_rel = -1;
  for(int tid = 0; tid < num_odes * NSP * NSP; ++tid)
  {
      if (save_jac[tid] != 0.0)
      {
          double err = fabs(save_jac[tid] - save_jac_multithread[tid]);
          if (err > max_err)
            max_err = err;
          err = err * 100.0 / fabs(save_jac[tid]);
          if (err > max_err_rel)
            max_err_rel = err;
      }
  }
  printf("Maximum absolute error: %e\nMaximum relative error: %e\n", max_err, max_err_rel);

  free(y_host);
  free(var_host);
  free(save_jac);
  free(save_jac_multithread);
  return 0;
}
