"""
A python script that runs a .c program which computes PI using the Monte Carlo method
and generates 2 .csv with the results

"""
import subprocess
import pandas as pd
import time
import logging


def get_weakly_DNA_openmp():

    """
    run tests for weak scaling measure
    :return: None
    """
    global points
    cores = [1, 2, 4, 8, 16]  # the number of cores/threads to be run the program
    exec_times_accumulator = []
    # file = "DNA1GB.txt"
    # file = "DNA2GB.txt"
    # file = "DNA4GB.txt"
    file = "DNA8GB.txt"
    file_size = 0
    start_time = time.time()

    for core in cores:
        sum_exec_time = 0
        file_size = file.split('GB')[0].split('DNA')[1]
        for i in range(10):  # execute the same program 10 times and compute averages
            output = subprocess.check_output(['./dna', file, str(core), file_size])  # the output from .c program is:
            # "time: ,pi: ,trials :"
            sum_exec_time += float(output.decode().split(',')[0].split(':')[1])

        exec_times_accumulator.append(sum_exec_time / 10)
        print("# cores:{}, file{}, file_size:{} :time:{}".format(core, file, file_size, sum_exec_time / 10))

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=[file], index=cores)

    df_exec_times.to_csv("exec_times_openmp_dna_{}_weakly.csv".format(file))

    print("Execution time:{} mins".format((time.time() - start_time) / 60))


def get_results_DNA_openmp():
    files = ["DNA1GB.txt", "DNA2GB.txt", "DNA4GB.txt", "DNA8GB.txt"]  # the number of data points to be generated
    cores = [1, 2, 4, 8, 16, 24]  # the number of cores/threads to be run the program
    exec_times_accumulator = []
    file_size = 0
    start_time = time.time()

    for core in cores:
        exec_times_arr = []
        for file in files:
            file_size = file.split('GB')[0].split('DNA')[1]
            sum_exec_time = 0
            for i in range(10):  # execute the same program 10 times and compute averages
                output = subprocess.check_output(['./dna', file, str(core), file_size])  # the output from .c program is:
                # "time: "
                sum_exec_time += float(output.decode().split(',')[0].split(':')[1])

            exec_times_arr.append(sum_exec_time/10)
            print("# cores:{}, file{}, file_size:{} :time:{}".format(core, file, file_size, sum_exec_time/10))

        exec_times_accumulator.append(exec_times_arr)

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=files, index=cores)

    df_exec_times.to_csv("exec_times_openmp_dna.csv")

    print("Execution time:{} mins".format((time.time()-start_time)/60))


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


def get_results_cuda():
    # data_points = [1E8, 1E9, 1E10]  # the number of data points to be generated
    global exec_times_arr, pi_values_arr
    # points = 1E8
    # points = 1E9
    points = 1E10
    exec_times_accumulator = []
    pi_values_accumulator = []
    cores = [1, 2, 4, 8, 16, 24, 32]  # the number of cores/threads to be run the program
    VMS = range(1, 9)

    start_time = time.time()
    for vms in range(1, 9):  # run it on 1-8 VMs
        exec_times_arr = []
        pi_values_arr = []

        for core in cores:
            sum_exec_time = 0
            sum_pi = 0
            for i in range(10):  # execute the same program 10 times and compute averages
                output = subprocess.check_output(['./cuda-pi', str(points), str(core), str(vms)])  # the output from .c program is:
                # "time: ,pi: "
                sum_exec_time += float(output.decode().split(',')[0].split(':')[1])
                sum_pi += float(output.decode().split(',')[1].split(':')[1])

            print("# vms:{}, threads:{} points{}, :time:{}, pi={}".format(vms, core, points, sum_exec_time/10, sum_pi/10))
            exec_times_arr.append(sum_exec_time / 10)
            pi_values_arr.append(sum_pi / 10)

        exec_times_accumulator.append(exec_times_arr)
        pi_values_accumulator.append(pi_values_arr)

    print("Execution time:{} mins".format((time.time()-start_time)/60))

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=cores, index=VMS)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=cores, index=VMS)

    df_exec_times.to_csv("exec_times_cuda_pi_{}.csv".format(points))
    df_pi_values.to_csv("pi_values_cuda_{}.csv".format(points))


def get_weakly_openmp():
    """
    run tests for weak scaling measure
    :return: None
    """
    global points
    cores = [1, 2, 4, 8, 16, 24]  # the number of cores/threads to be run the program
    exec_times_accumulator = []
    pi_values_accumulator = []
    # data_points = 1E8
    # data_points = 1E9
    data_points = 1E10  # TODO:  won't run it
    start_time = time.time()

    for core in cores:
        sum_exec_time = 0
        sum_pi = 0
        for i in range(10):  # execute the same program 10 times and compute averages
            points = core * data_points
            output = subprocess.check_output(['./openmp', str(points), str(core)])  # the output from .c program is:
            # "time: ,pi: ,trials :"
            sum_exec_time += float(output.decode().split(',')[0].split(':')[1])
            sum_pi += float(output.decode().split(',')[1].split(':')[1])

        exec_times_accumulator.append(sum_exec_time/10)
        pi_values_accumulator.append(sum_pi/10)
        print("# cores:{}, points{}, :time:{}, pi={}".format(core, points, sum_exec_time/10, sum_pi/10))

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=[data_points], index=cores)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=[data_points], index=cores)

    df_exec_times.to_csv("exec_times_openmp_pi_1E10_weakly.csv")
    df_pi_values.to_csv("pi_values_openmp_1E10_weakly.csv")

    print("Execution time:{} mins".format((time.time()-start_time)/60))


def get_weakly_mpi():
    """
    run tests for weak scaling measure
    :return: None
    """
    # data_points = 1E8  # the number of data points to be generated
    # data_points = 1E9
    data_points = 1E10 #TODO:  won't run it

    VMS = range(1, 9)
    exec_times_accumulator = []
    pi_values_accumulator = []

    start_time = time.time()

    for vms in range(1, 9):  # run it on 1-8 VMs
        points = vms * data_points
        sum_exec_time = 0
        sum_pi = 0
        for i in range(10):  # execute the same program 10 times and compute averages
            output = subprocess.check_output(['mpirun', '-np', '{}'.format(str(vms)), './mpi', str(points)])  # the output from .c program is:
            # "time: ,pi: "
            sum_exec_time += float(output.decode().split(',')[0].split(':')[1])
            sum_pi += float(output.decode().split(',')[1].split(':')[1])

        exec_times_accumulator.append(sum_exec_time/10)
        pi_values_accumulator.append(sum_pi/10)

        print("# vms:{}, points{}, :time:{}, pi={}".format(vms, points, sum_exec_time/10, sum_pi/10))

    print("Execution time:{} mins".format((time.time()-start_time)/60))

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=[data_points], index=VMS)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=[data_points], index=VMS)

    df_exec_times.to_csv("exec_times_mpi_pi_1E9_weakly.csv")
    df_pi_values.to_csv("pi_values_mpi_1E9_weakly.csv")


def get_weakly_cuda():
    """
    run tests for weak scaling measure
    :return: None
    """
    # data_points = [1E8, 1E9, 1E10]  # the number of data points to be generated
    # data_points = 1E8
    # data_points = 1E9
    data_points = 1E10  #TODO: we won't run it for now
    cores = [1, 2, 4, 8, 16, 24, 32]  # the number of cores/threads to be run the program
    VMS = range(1, 9)

    exec_times_accumulator = []
    pi_values_accumulator = []
    start_time = time.time()

    for vms in range(1, 9):  # run it on 1-8 VMs
        exec_times_arr = []
        pi_values_arr = []

        for core in cores:
            points = vms * data_points
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

    df_exec_times = pd.DataFrame(data=exec_times_accumulator, columns=cores, index=VMS)
    df_pi_values = pd.DataFrame(data=pi_values_accumulator, columns=cores, index=VMS)

    df_exec_times.to_csv("exec_times_cuda_pi_1E8_weakly.csv")
    df_pi_values.to_csv("pi_values_cuda_1E8_weakly.csv")
    print("Dataframes saved!")


if __name__ == "__main__":
    logging.basicConfig(filename="log_dna.log",
                        filemode="a",
                        format='%(levelname)s - %(asctime)s - %(message)s',
                        level=logging.DEBUG)

    # get_results_openmp()
    # get_results_mpi()
    # get_results_cuda()

    # get_weakly_openmp()
    # get_weakly_mpi()
    # get_weakly_cuda()

    # get_results_DNA_openmp()

    get_weakly_DNA_openmp()

