// This program is to caculate PI using MPI
// The algorithm is based on Monte Carlo method. 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
#include <sys/time.h>

#define FPTYPE double


int main (int argc, char* argv[])
{
    long long int ndata_points=0, result=0, sum=0, i; 
    int rank, error, size;
    double pi=0.0, begin=0.0, end=0.0, x, y;
    struct drand48_data buffer;
    char *value = argv[1];

    ndata_points = atoll(value);

    //error=MPI_Init (&argc, &argv);
    MPI_Init(NULL, NULL);

    //Get process ID
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);
    
    //Get processes Number
    MPI_Comm_size (MPI_COMM_WORLD, &size);
    
    //Synchronize all processes and get the begin time
    MPI_Barrier(MPI_COMM_WORLD);
    begin = MPI_Wtime();
    
    unsigned int seed = ((time(NULL)) ^ rank);


    //Each process will caculate a part of the sum
    for (i=rank; i<ndata_points; i+=size)
    {
        FPTYPE x = (FPTYPE)rand_r(&seed)/RAND_MAX;
        FPTYPE y = (FPTYPE)rand_r(&seed)/RAND_MAX;
        if(x*x+y*y<1.0)
            result++;
    }
    
    //Sum up all results
    MPI_Reduce(&result, &sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    
    //Synchronize all processes and get the end time
    MPI_Barrier(MPI_COMM_WORLD);
    end = MPI_Wtime();
    
    //Caculate and print PI
    if (rank==0)
    {
        pi=4*(FPTYPE)sum/ndata_points;
        printf("time:%g,pi:%g \n", end-begin, pi);
    }


    error=MPI_Finalize();
    
    return 0;
}