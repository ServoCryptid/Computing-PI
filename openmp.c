/* Program to compute Pi using Monte Carlo methods */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <omp.h>

#define FPTYPE double //TODO: why?

static double rtclock(){
   struct timeval Tp;
   gettimeofday (&Tp, NULL);
   return (Tp.tv_sec + Tp.tv_usec * 1.0e-6);
}

int main(int argc, char* argv[])
{  

   char *value = argv[1], *value2 = argv[2];    //first arg is the # of points, second arg is the #of threads
   int nthreads;
   long long int niter, ndata_points;
   long long int i,count=0; 
   FPTYPE pi;
   double startt, stopt;

   ndata_points = atoll(value);
   nthreads = atoi(value2);

   niter = ndata_points/nthreads;

   startt = rtclock();

   /* initialize random numbers */
   count=0;

#pragma omp parallel
   {
      unsigned int seed = ((time(NULL)) ^ omp_get_thread_num());

#pragma omp for private(i) reduction(+:count) schedule(dynamic) 
      for ( i=0; i<niter; i++) {
         FPTYPE x = (FPTYPE)rand_r(&seed)/RAND_MAX;
         FPTYPE y = (FPTYPE)rand_r(&seed)/RAND_MAX;
         if (x*x+y*y<=1) count++;
      }
   }
   pi=4*(FPTYPE)count/niter;

   stopt = rtclock();
   
   printf("time:%g,pi:%g \n", stopt-startt, pi);

   return 0;
}