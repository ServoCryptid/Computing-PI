// the code for generating PI using monte carlo
#include <omp.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <math.h>
#define SEED 35791246

int points_generation_rand(long int niter){ //the first attempt, rand() is not thread safe!
	int j, count=0;
	double x,y;

   /* initialize random numbers */
   srand(SEED);

	for (j=0; j<niter; j++){
		x = (double)rand()/RAND_MAX; //rand() is not thread safe; try different implementations
		y = (double)rand()/RAND_MAX;
		if (x*x+y*y<1) count++; 
	}

	return count;
}


int points_generation_drand48_r(long int niter){
	int j, count=0;
	struct drand48_data buffer;
	double x,y;

   /* initialize random numbers */
   srand48_r(SEED, &buffer);

	for (j=0; j<niter; j++){
		drand48_r(&buffer, &x);
		drand48_r(&buffer, &y);
		if (x*x+y*y<1) count++; 
	}

	return count;
}


main(int argc, char* argv[])
{
   long int ndata_points=0; 
   int nthreads;
   long int niter;
   long int i, j, count=0; /* # of points in the 1st quadrant of unit circle */
   double pi;
   char *value = argv[1]; 	//first arg is the # of points
   
   clock_t begin = clock(); //is it ok to start timer here?

   ndata_points = atoi(value);

   nthreads = omp_get_max_threads();

   niter = ndata_points/nthreads;

   #pragma omp parallel for shared(niter) reduction(+:count)
   for (i=0; i<nthreads; i++) { 
   		count += points_generation_drand48_r(niter);
    }

   	pi= 4 * (double)count/ndata_points;

   	printf("# of trials= %d , estimate of pi is %g, exec. time %g seconds \n",
   			niter,pi,(double)(clock() - begin)/CLOCKS_PER_SEC);

   	return 0;
}	