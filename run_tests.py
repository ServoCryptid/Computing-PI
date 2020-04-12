"""
A python script that runs a .c program which computes PI using the Monte Carlo method
and generates 2 .csv with the results

"""
import subprocess
import pandas as pd


def get_results():
    data_points = [100000000, 1000000000, 10000000000]  # the number of data points to be generated
    # cores = [1, 2, 4, 8, 16, 32]  # the number of cores to be run the program
    cores = [1, 2]  # the number of cores to be run the program
    exec_times_accumulator = []
    pi_values_accumulator = []

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

                print("time:{}, pi={}".format(sum_exec_time, sum_pi))

            exec_times_arr.append(sum_exec_time/10)
            pi_values_arr.append(sum_pi/10)

        exec_times_accumulator.append(exec_times_arr)
        pi_values_accumulator.append(pi_values_arr)

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=data_points, index=cores)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=data_points, index=cores)

    df_exec_times.to_csv("exec_times_openmp_pi.csv")
    df_pi_values.to_csv("pi_values_openmp.csv")


if __name__ == "__main__":

    get_results()
