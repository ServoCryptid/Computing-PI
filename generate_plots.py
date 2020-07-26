'''
Script which generates the plots(scalability plots – weak and strong, parallel efficiency) needed for the BDT report
'''
import pandas as pd
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
import os


def compute_values_cuda(path):
    data_points = ['1E8', '1E9', '1E10']
    df = pd.DataFrame()
    for points in data_points:
        df_cuda = pd.read_csv(join(path, f"exec_times_cuda_pi_{points}.csv"))
        df_cuda.set_index(df_cuda.iloc[:, 0], inplace=True)  # set the index to be the #cores
        df_cuda.drop(df_cuda.columns[0], axis=1, inplace=True)  # remove the number of cores column

        values = pd.Series(np.diag(df_cuda), index=df_cuda.columns.astype(int)) # the first diagonal values eg: 1 block-1thread, 2blocks-2threads each...
        df[points] = values

    print(df.index)
    df_speedup = df.transform(lambda col: col.iloc[0]/col)
    df_speedup.to_csv(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\cuda\strong_scaling.csv",
              index_label="Cores")

    df = df_speedup.transform(lambda col: col/col.index.values, axis=0)
    blocks = list(range(1, 8))
    df = df.transform(lambda col: col/blocks)
    df.to_csv(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\cuda\parallel.csv",
              index_label="Cores")

    #for weak scaling
    #first we concat the columns
    data_points = ['1E8', '1E9']
    df = pd.DataFrame()
    for points in data_points:
        col = pd.read_csv(join(path, f"exec_times_cuda_pi_{points}_weakly.csv"))
        col.set_index(col.iloc[:, 0], inplace=True)  # set the index to be the #cores
        col.drop(col.columns[0], axis=1, inplace=True)  # remove the number of cores column
        df[points] = pd.Series(np.diag(col), index=col.columns.astype(int))

    df = df.transform(lambda col: col.iloc[0]/col)
    blocks = list(range(1, 8))
    df = df.transform(lambda col: col/blocks)
    df.to_csv(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\cuda\weak_scaling.csv", index_label='Cores')
    print(df)


def compute_values_mpi(path):
    df_mpi = pd.read_csv(join(path, "exec_times_mpi_pi.csv"))

    df_mpi.set_index(df_mpi.iloc[:, 0], inplace=True)  # set the index to be the #cores
    df_mpi.drop(df_mpi.columns[0], axis=1, inplace=True)  # remove the number of cores column

    df_mpi.columns = ['1E8', '1E9', '1E10']  # set the column name for consistency
    df_speedup = df_mpi.transform(lambda col: col.iloc[0] / col)
    df_speedup.to_csv(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\mpi\strong_scaling.csv",
                      index_label="Cores")
    print(df_speedup)

    df_parallel = df_speedup.transform(lambda col: col/df_speedup.index.values, axis=0)

    df_parallel.to_csv(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\mpi\parallel.csv",
                       index_label="Cores")
    print(df_parallel)

    #for weak scaling
    #first we concat the columns
    data_points = ['1E8', '1E9']
    df = pd.DataFrame()
    for points in data_points:
        col = pd.read_csv(join(path, f"exec_times_mpi_pi_{points}_weakly.csv"))
        col.set_index(col.iloc[:, 0], inplace=True)  # set the index to be the #cores
        col.drop(col.columns[0], axis=1, inplace=True)  # remove the number of cores column
        df[points] = pd.Series(col.iloc[:, 0], index=col.index.astype(int))

    df = df.transform(lambda col: col.iloc[0]/col)
    df.to_csv(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\mpi\weak_scaling.csv", index_label='Cores')
    print(df)


def compute_values_openmp(path, path_for_csv, algo, cols):
    df_openmp = pd.read_csv(join(path, f"exec_times_openmp_{algo}.csv"))

    df_openmp.set_index(df_openmp.iloc[:, 0], inplace=True)  # set the index to be the #cores
    df_openmp.drop(df_openmp.columns[0], axis=1, inplace=True)  # remove the number of cores column

    df_openmp.columns = cols
    df_speedup = df_openmp.transform(lambda col: col.iloc[0] / col)
    df_speedup.to_csv(f"{path_for_csv}/strong_scaling.csv", index_label="Cores")
    print(df_speedup)

    df_parallel = df_speedup.transform(lambda col: col/df_speedup.index.values, axis=0)

    df_parallel.to_csv(f"{path_for_csv}/parallel.csv",
                       index_label="Cores")
    print(df_parallel)

    #for weak scaling
    # first we concat the columns
    df = pd.DataFrame()
    for c in cols:
        col = pd.read_csv(join(path, f"exec_times_openmp_{algo}_{c}_weakly.csv"))
        col.set_index(col.iloc[:, 0], inplace=True)  # set the index to be the #cores
        col.drop(col.columns[0], axis=1, inplace=True)  # remove the number of cores column
        df[c] = pd.Series(col.iloc[:, 0], index=col.index.astype(int))

    df = df.transform(lambda col: col.iloc[0]/col)
    df.to_csv(f"{path_for_csv}/weak_scaling.csv", index_label='Cores')
    print(df)


def plot_scenario(name, fig_name, path_omp, path_mpi, path_cuda, algo):
    """

    :param name: strong scaling, weak scaling or parallel efficiency
    :return:
    """
    df_openmp = pd.DataFrame()
    df_mpi = pd.DataFrame
    df_cuda = pd.DataFrame()

    if name == "Strong Scaling":
        if os.path.exists(f"{path_omp}\strong_scaling.csv"):
            df_openmp = pd.read_csv(f"{path_omp}\strong_scaling.csv", index_col='Cores')

        if os.path.exists(f"{path_mpi}/strong_scaling.csv"):
            df_mpi = pd.read_csv(f"{path_mpi}/strong_scaling.csv", index_col='Cores')

        if os.path.exists(f"{path_cuda}/strong_scaling.csv"):
            df_cuda = pd.read_csv(f"{path_cuda}/strong_scaling.csv", index_col='Cores')
    elif name == "Parallel Efficiency":
        if os.path.exists(f"{path_omp}\parallel.csv"):
            df_openmp = pd.read_csv(f"{path_omp}\parallel.csv", index_col='Cores')

        if os.path.exists(f"{path_mpi}/parallel.csv"):
            df_mpi = pd.read_csv(f"{path_mpi}/parallel.csv", index_col='Cores')

        if os.path.exists(f"{path_cuda}/parallel.csv"):
            df_cuda = pd.read_csv(f"{path_cuda}/parallel.csv", index_col='Cores')
    else:
        if os.path.exists(f"{path_omp}\weak_scaling.csv"):
            df_openmp = pd.read_csv(f"{path_omp}\weak_scaling.csv", index_col='Cores')

        if os.path.exists(f"{path_mpi}/weak_scaling.csv"):
            df_mpi = pd.read_csv(f"{path_mpi}/weak_scaling.csv", index_col='Cores')

        if os.path.exists(f"{path_cuda}/weak_scaling.csv"):
            df_cuda = pd.read_csv(f"{path_cuda}/weak_scaling.csv", index_col='Cores')

    cols = df_openmp.columns
    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')
    line_style = ['-', '-', '--', '-']
    markers = ['s', 'o', '', '*']
    index = 0
    index2 = 0
    print(cols)
    for col in cols:
        if not df_openmp.empty:
            plt.plot(df_openmp.index.values, df_openmp[col], line_style[index], marker=markers[index], color=palette(index2), linewidth=1.5, alpha=0.9, label=f'OMP{col}')
            plt.title(f"{name}", loc='left', fontsize=14, fontweight=0, color='orange')
            index2 += 1

        if not df_mpi.empty:
            plt.plot(df_mpi.index.values, df_mpi[col], line_style[index], marker=markers[index], color=palette(index2), linewidth=1.5, alpha=0.9, label=f'MPI{col}')
            plt.title(f"{name}", loc='left', fontsize=14, fontweight=0, color='orange')
            index2 += 1

        if not df_cuda.empty:
            plt.plot(df_cuda.index.values, df_cuda[col], line_style[index], marker=markers[index], color=palette(index2), linewidth=2, alpha=0.9, label=f'CUDA{col}')
            plt.title(f"{name}", loc='left', fontsize=14, fontweight=0, color='orange')
            index2 += 1

        if name != "Strong Scaling":
            plt.axhline(y=1, color='y', linestyle='-', linewidth=1)
            plt.ylim(-6, 8)

        index += 1

    if name != 'Weak scaling':
        # Add legend
        plt.legend(ncol=3)

        plt.xlabel("Cores")
        plt.ylabel("Speedup")
    else:
        # Add legend
        plt.legend(ncol=2)
        plt.xlabel("GB/core")
        plt.ylabel("speedup")

    plt.xticks(df_openmp.index.values)
    plt.savefig(r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\plots\{}\{}".format(algo, f"{fig_name}_{algo}"))
    plt.show()


if __name__ == "__main__":
    path_openmp = r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp"
    path_mpi = r"C:\Users\larisa.biriescu\Facultate\BDT\PI\mpi\results\mpi_ver4"
    path_cuda = r"C:\Users\larisa.biriescu\Facultate\BDT\PI\cuda\results\cuda_ver2"

    #speedup = time seq algo/time parallel algo
    #strong scaling: speedup =  when data is constant, different number of cores. eg: 1M datapoints-1core, 1M datapoints-2ores

    #weak scaling: speedup when data/resource is kept constant. eg: 1M datapoints-1core, 2M datapoints-2cores

    #parallel efficiency = speedup/# of cores

    compute_values_openmp(f"{path_openmp}/pi", r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\dna",
                              "pi", ['1E8', '1E9', '1E10'])
    compute_values_mpi(path_mpi)
    compute_values_cuda(path_cuda)

    plot_scenario("Strong Scaling", 'strong_scaling',
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\pi",
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\mpi",
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\cuda",
                  'pi')
    plot_scenario("Parallel Efficiency", 'parallel_efficiency',
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\pi",
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\mpi",
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\cuda",
                  'pi')
    plot_scenario("Weak scaling", 'weak_scaling',
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\pi",
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\mpi",
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\cuda",
                  'pi')

    compute_values_openmp(f"{path_openmp}\dna", r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\dna",
                          "dna", ["DNA1GB", "DNA2GB", "DNA4GB", "DNA8GB"])
    plot_scenario("Strong Scaling", 'strong_scaling',
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\dna",
                  r"",
                  r"",
                  'dna')
    plot_scenario("Parallel Efficiency", 'parallel_efficiency',
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\dna",
                  r"",
                  r"",
                  'dna')
    plot_scenario("Weak scaling", 'weak_scaling',
                  r"C:\Users\larisa.biriescu\Facultate\BDT\GITHUB\Computing-PI\results\openmp\dna",
                  r"",
                  r"",
                  'dna')

