"""
A python script that runs a .c program which computes PI using the Monte Carlo method
and generates 2 .csv with the results

"""
import subprocess
import pandas as pd
import time


def get_results_openmp():
    data_points = [100000000, 1000000000, 10000000000]  # the number of data points to be generated
    cores = [1, 2, 4, 8, 16, 24, 32]  # the number of cores/threads to be run the program
    exec_times_accumulator = []
    pi_values_accumulator = []

    start_time = time.time()

    for core in cores:
        exec_times_arr = []
        pi_values_arr = []
        for points in data_points:
            sum_exec_time = 0
            sum_pi = 0
            for i in range(10):  # execute the same program 10 times and compute averages
                output = subprocess.check_output(['./openmp', str(points), str(core)])  # the output from .c program is:
                # "time: ,pi: ,trials :"
                sum_exec_time += float(output.decode().split(',')[0].split(':')[1])
                sum_pi += float(output.decode().split(',')[1].split(':')[1])

            exec_times_arr.append(sum_exec_time/10)
            pi_values_arr.append(sum_pi/10)
            print("# cores:{}, points{}, :time:{}, pi={}".format(core, points, sum_exec_time/10, sum_pi/10))

        exec_times_accumulator.append(exec_times_arr)
        pi_values_accumulator.append(pi_values_arr)

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=data_points, index=cores)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=data_points, index=cores)

    df_exec_times.to_csv("exec_times_openmp_pi.csv")
    df_pi_values.to_csv("pi_values_openmp.csv")

    print("Execution time:{} mins".format((time.time()-start_time)/60))

    # subprocess.call(["gcloud config set compute/zone", " us-central1-c"])  # set the timezone to not be asked each time
    # subprocess.call(["gcloud compute scp", "omp:~/exec_times_openmp_pi.csv",
    #                  r"C:\Users\larisa.biriescu\Facultate\BDT\open_mp\results"])
    # subprocess.call(["gcloud compute scp", "omp:~/pi_values_openmp.csv",
    #                  r"C:\Users\larisa.biriescu\Facultate\BDT\open_mp\results"])


def get_results_cuda():
    data_points = [1E8, 1E9, 1E10]  # the number of data points to be generated
    # VMS = range(1, 9)
    VMS = [1]
    # cores = [1, 2, 4, 8, 16, 24, 32]  # the number of cores/threads to be run the program
    cores = [32]  # the number of cores/threads to be run the program

    # for vms in range(1, 9):  # run it on 1-8 VMs
    for vms in range(1, 3):  # run it on 1-8 VMs
        start_time = time.time()

        exec_times_accumulator = []
        pi_values_accumulator = []
        for core in cores:
            exec_times_arr = []
            pi_values_arr = []
            for points in data_points:
                sum_exec_time = 0
                sum_pi = 0
                for i in range(10):  # execute the same program 10 times and compute averages
                    output = subprocess.check_output(['./cuda-pi', str(points), str(core), str(vms)])  # the output from .c program is:
                    # "time: ,pi: "
                    sum_exec_time += float(output.decode().split(',')[0].split(':')[1])
                    sum_pi += float(output.decode().split(',')[1].split(':')[1])

                exec_times_arr.append(sum_exec_time/10)
                pi_values_arr.append(sum_pi/10)

                print("# vms:{}, threads:{} points{}, :time:{}, pi={}".format(vms, core, points, sum_exec_time/10, sum_pi/10))

            exec_times_accumulator.append(exec_times_arr)
            pi_values_accumulator.append(pi_values_arr)

        print("Execution time:{} mins".format((time.time()-start_time)/60))

        df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=data_points, index=cores)
        df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=data_points, index=cores)

        df_exec_times.to_csv("exec_times_mpi_pi_{}.csv".format(vms))
        df_pi_values.to_csv("pi_values_mpi_{}.csv".format(vms))
        print("Dataframes saved!")


def get_results_mpi():
    data_points = [1E8, 1E9, 1E10]  # the number of data points to be generated
    VMS = range(1, 9)
    exec_times_accumulator = []
    pi_values_accumulator = []

    start_time = time.time()

    for vms in range(1, 9):  # run it on 1-8 VMs
        exec_times_arr = []
        pi_values_arr = []
        for points in data_points:
            sum_exec_time = 0
            sum_pi = 0
            for i in range(10):  # execute the same program 10 times and compute averages
                output = subprocess.check_output(['mpirun', '-np', '{}'.format(str(vms)), './mpi', str(points)])  # the output from .c program is:
                # "time: ,pi: "
                sum_exec_time += float(output.decode().split(',')[0].split(':')[1])
                sum_pi += float(output.decode().split(',')[1].split(':')[1])

            exec_times_arr.append(sum_exec_time/10)
            pi_values_arr.append(sum_pi/10)

            print("# vms:{}, points{}, :time:{}, pi={}".format(vms, points, sum_exec_time/10, sum_pi/10))

        exec_times_accumulator.append(exec_times_arr)
        pi_values_accumulator.append(pi_values_arr)

    print("Execution time:{} mins".format((time.time()-start_time)/60))

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=data_points, index=VMS)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=data_points, index=VMS)

    df_exec_times.to_csv("exec_times_mpi_pi.csv")
    df_pi_values.to_csv("pi_values_mpi.csv")


if __name__ == "__main__":

    # get_results_openmp()
    # get_results_mpi()
    get_results_cuda()