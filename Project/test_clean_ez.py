# system imports
import io
import time
import os
import itertools as it
from os.path import abspath, join, dirname, basename
import sys
import cProfile
import pstats


# third party imports
import numpy as np
import matplotlib.pyplot as plt


# import the path to the package
project_dir = abspath(join(dirname(__file__), '..'))
# project_dir = abspath(join(dirname(__file__), user_dir, '/t0veccproj/'))
sys.path.insert(0, project_dir)
import project

# local imports
from project.vibronic_hamiltonian import vibronic_hamiltonian
from project.vibronic import vIO, VMK, model_op
import project.spectra
import project.log_conf

# assert len(sys.argv) == 6, f"{len(sys.argv)=}"
# nZ, nH, ntf, job_name, root = sys.argv[1:]
# nZ, nH, ntf = int(nZ), int(nH), int(ntf)
# print(type(nZ), type(nH), type(ntf), type(job_name))

assert len(sys.argv) == 5, f"{len(sys.argv)=}"
nZ, nH, ntf, file_name = sys.argv[1:]
nZ, nH, ntf = int(nZ), int(nH), int(ntf)
print(type(nZ), type(nH), type(ntf), type(file_name))


# nZ is the truncation of the T operator NOT the taylor
order_dict = {
    0: "constant",
    1: "linear",
    2: "quadratic",
    3: "cubic",
    4: "quartic",
}

root_directory = os.getcwd()
root = root_directory  # modify later if want to make arg pass

# file_name = "RhF3_Z2_H1_10000fs"

job_name = f"{file_name:s}_T{nZ:d}_H{nH:d}"


def process_data(filename):
    """ temporary formatted printing of profiling data """
    try:
        s = io.StringIO()
        p = pstats.Stats(filename, stream=s)
        # p.strip_dirs().sort_stats("tottime").print_stats(2)
        p.strip_dirs().sort_stats("tottime").print_stats(10)
        p.strip_dirs().sort_stats("cumulative").print_stats(20)
        p.strip_dirs().sort_stats("cumulative").print_stats('contract', 100)
        # p.strip_dirs().sort_stats("cumulative").print_callees('contract_expression')

        with open(filename+".txt", "w+") as f:
            s = io.StringIO()
            p = pstats.Stats(filename)
            p.strip_dirs().sort_stats("tottime").print_stats(2)
            p.strip_dirs().sort_stats("tottime").print_stats(6)
            p.strip_dirs().sort_stats("cumulative").print_stats(20)
            p.strip_dirs().sort_stats("cumulative").print_stats('calculate', 15)
            p.strip_dirs().sort_stats("cumulative").print_callees('_calculate_order_4_w_operator_optimized')
            f.write(s.getvalue())

    except Exception:
        print("cProfile data is not stored properly!")

    def print_based_on_criteria():
        # just example code, isn't called anywhere
        spec = "{title:^90}\n" + f"{'':*>90s}" + "\n{data}"
        string_list = []

        for title, criteria in [
            ("Highest # of calls", "calls"),
            ("Highest cumulative time", "cumulative"),
            # ("Highest percall time", "pcalls"),
            ("Highest tottime", "tottime")
        ]:
            s = io.StringIO()
            p = pstats.Stats(filename, stream=s)
            p.strip_dirs().sort_stats(criteria).print_stats(10)
            print(spec.format(
                title=title,
                data="\n".join(s.getvalue().splitlines()[7:])
            ))

    return


def generate_acf_data(model, file_name, order, t_final=10.0, nof_steps=int(1e4), FC=False, compare_FCI=False):
    """ x """

    #hamiltonian = vibronic_hamiltonian(model, file_name, H_order=order, T_order=nZ, CC_order=2)
    hamiltonian = vibronic_hamiltonian(
        model, file_name,
        hamiltonian_truncation_order=order, cc_truncation_order=order,
        T_truncation_order=1, Z_truncation_order=nZ,
        calculate_population_flag=False,
    )
    # run coupled cluster propagation
    if (profiling := False):
        filename = f"cProfile_{file_name}_{order_dict[order]}_tf{int(t_final):}_t0VECC_"
        filename += "_ST_VECC_{:}_22_06_24".format(hamiltonian.T_truncation_order)

        func_string = 'hamiltonian.rk45_integration(t_final=t_final, nof_points=nof_steps)'
        cProfile.runctx(
            func_string,
            globals(),
            locals(),
            filename
        )
        process_data(filename)
        sys.exit(0)

    else:
        start_time = time.time()
        hamiltonian.rk45_integration(t_final=t_final, nof_points=nof_steps)
        end_time = time.time()
        print(f"Very simple timing:   {end_time - start_time:10.4f}")

    # make plot and store data
    output_path = hamiltonian.save_acf_data(file_name=file_name, output_path=root_directory)
    hamiltonian.plot_acf(file_name=file_name, output_path=root_directory)

     
    file_path_ABS = join(root_directory,f"Norm{file_name}.txt")
    hamiltonian._save_data(file_path_ABS, hamiltonian.t_cc, hamiltonian.Norm_cc[:,0])

    return output_path


def gnuplot_spectrum(*args):
    """ a """

    # unpack arguments
    exec_name, normalized_path_ABS, model_name, order, t, FC = args

    left_eV, right_eV = -2, 2
    min_y, max_y = -3, 60
    nof_points = 13000
    tau = 40
    iexp = 1

    fc_string = "FC" if FC else "vibronic"

    # fourier transform
    command = (
        "#~/LOCAL/mctdh/mctdh86.4/bin/binary/x86_64/autospec86 "
        # "-g 1 "  # to print gnuplot commands or not
        f"-o {exec_name:s}.pl "
        f"-f {normalized_path_ABS:s} "
        f"-p {nof_points:d} "
        # f"-EP "
        # f"-e {harmonic_ground_state} eV " # x axis shift (left/right) to account for H.O. G.S.
        f"{left_eV} {right_eV} ev "  # x axis limits (in eV)
        f"{tau:d} "   # tau value
        f"{iexp:d} "  # iexp value
    )
    #     # "output_filename": join(root_directory, exec_name + ".pl"),
    #     "output_filename": "./" + exec_name + ".pl",
    #     "input_filename": "./" + normalized_path,
    #     "nof_points": nof_points,
    #     "left_eV": left_eV,
    #     "right_eV": right_eV,
    #     "tau": tau,
    #     "iexp": iexp,
    #     # 'g3': True
    # })
    #os.system(command)   # execute autospec84

    # same thing for MCTDH
    # command = project.spectra.generate_mctdh_pl(**{
    #     # "output_filename": join(root_directory, exec_name + ".pl"),
    #     "output_filename": f"./MCTDH_{fc_string}_{order_dict[order]}.pl",
    #     "input_filename": f"./auto_{fc_string}_{order_dict[order]}",
    #     # "output_filename": f"./SOS.pl",
    #     # "input_filename": f"./ACF_SOS_h2o_FC_40BF_tf50.txt",
    #     "nof_points": nof_points,
    #     "left_eV": left_eV,
    #     "right_eV": right_eV,
    #     "tau": tau,
    #     "iexp": iexp,
    # })
    #
    print(command)
    # os.system(command)   # execute autospec84

    # doctor the file name to make it look better in the plot
    plot_title = model_name.replace('_', ' ').replace('h2o', 'h_{2}o')

    size = [1200, 800]

    # output_file = f'{root_directory}/cc_spectrum_{model_name:s}_{nof_points:d}_{tau:d}tau.png'
    output_file = f'{root_directory}/cc_spectrum_{model_name:s}.png'

    plotting_command = '\n'.join([
        f"set terminal png size {size[0]},{size[1]}",
        # f"set output './spectrum_{model_name:s}_{nof_points:d}_{t_final:d}fs_{tau:d}tau_{nof_BF}SOSBF_{mctdh_BF}MCTDHBF.png'",
        f"set output '{output_file:s}'",
        # "set style data line",
        "set nologscale", "set xzeroaxis", "set xlabel 'Energy[eV]'",
        f"set xr [ {left_eV}: {right_eV}]",
        f"set yr [ {min_y}: {max_y}]",
        f"set title '{plot_title:s} spectrum, n-cos = 1, tau: {tau:d}.0 1, {int(t):d}fs'",
        # "set style line 1 lt 2 lw 4 lc 'black'",
        # "set style line 2 lt 3 lw 2 lc 'red'",
        f"#plot '{root_directory}/op_NH36Q_3st_PBF30_tf250.00_auto_total' using 1:2 with lines ls 1 lc 'black' title 'MCTDH ({fc_string})'",
        f"plot \
            '{root_directory}/{exec_name}.pl' using 1:3 with lines ls 1 lc 'red' title 'CC',\
        ",
            # '{root_directory}/{exec_name}_6.pl' every 6 using 1:3 linetype 4 title '1E-6 1E-9 CC',\
            # '{root_directory}/{exec_name}_9.pl' every 6 using 1:3 linetype 3 title '1E-9 1E-12 CC',\
            # '{root_directory}/{exec_name}_12.pl' every 6 using 1:3 linetype 1 title '1E-12 1E-15 CC',\
    ])

    path_plotting_file = f"{root_directory}/spectrum_plotting.pl"

    # write the plotting commands to a file
    with open(path_plotting_file, 'w') as fp:
        fp.write(command)
        fp.write("\n")
        fp.write(plotting_command)

    return path_plotting_file


def write_acf_plotting_file(cc_file, cc_file2, FC, t_final, nof_points=5000):
    plotting_string = '\n'.join([
        # "set style circle radius graph 0.002",
        "set style line 1 lt 2 pt 12 ps 1 pi -1",
        # "set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 pi -1 ps 1.5",
        # "set pointintervalbox 2",
        "set terminal png size 1200,800",
        f"set output './ACF_{model_name:s}_{order_dict[order]}_{t_final:.0f}fs.png'",
        "set style data line",
        "set nologscale",
        "set xzeroaxis",
        # "set yr [ -3: 3]",
        # f"set multiplot layout 2,2",
        f"set title 'ACF comparison of {order_dict[order]} {model_name:s} {t_final:.0f}fs'",
        # top row (real)
        # "unset xtics", "unset xlabel",
        "set ylabel 'C(tau/hbar)'",
        f"set xr [ 0.0: {t_final:d}.0]",
        f"plot \
            '{cc_file}' us 1:2 lc 'green' title 'CC Real (raw RK45)',\
            '{cc_file2}' us 1:2 with linespoints ls 1 lc 'blue' title 'CC Real (interpolated)',\
        "
            # 'ACF_SOS_{file_name}_FC_40BF_tf50.txt' us 1:2 lc 'red' title 'SOS Real',\
            # '{root_directory}/auto_{fc_string}_{order_dict[order]}' us 1:2 with linespoints ls 4 ps 3 lc 'red' title 'MCTDH Real ({fc_string})',\
    ])

    plotting_file = "acf_plotting.pl"

    # write the plotting commands to a file
    with open(plotting_file, 'w') as fp:
        fp.write(plotting_string)

    return plotting_file


def get_model_from_op_file(path, order):
    """a wrapper function on top of Neil's I/O script to readin vibronic model parameter from standard op file"""
    raw_model = vIO.read_raw_model_op_file(
        path,
        get_transition_dipole_moment=True,
        surface_symmetrize=True,
        dimension_of_dipole_moments=3,
    )

    raw_model = vIO.model_remove_ground_state(raw_model)

    # when we symmetrize the surfaces we divide the diagonal by 2 (that already happens and works correctly)
    A, N = vIO._extract_dimensions_from_dictionary(raw_model)

    if order >= 2:  # includes quadratic terms
        model_op.mode_symmetrize_from_upper_triangle_quadratic_terms(N, range(A), raw_model[VMK.G2])
        # now the raw_model has been symmetrized in modes as well

    if False:  # divide all off-diagonal (vibrational) components by 2 (only if necessary)
        for i, j in it.product(range(N), range(N)):
            if i == j:
                continue
            raw_model[VMK.G2][i, j, :, :] /= 2

    # swap order of electron / vibrational dimensions (VECC uses different order for computational efficiency)
    vIO.prepare_model_for_cc_integration(raw_model, order)

    return raw_model


def get_model_from_json_file(path, order):
    """ x """

    model = vIO.load_model_from_JSON(path)

    A, N = vIO._extract_dimensions_from_dictionary(model)

    if False:  # if the model includes the ground state that you excited it from
        model = vIO.model_remove_ground_state(model)

    if False:  # divide all off-diagonal (electronic) components by 2 (only if necessary)
        for a, b in it.product(range(A), range(A)):
            if a == b:
                model[VMK.E][a, b] /= 2

    model[VMK.etdm].fill(complex(0.1))
    model[VMK.mtdm].fill(complex(0.1))

    # swap electron / vibrational dimensions
    vIO.prepare_model_for_cc_integration(model, order)

    return model


if (__name__ == '__main__'):

    use_JSON_flag = True
    FC = False

    t_final = float(ntf)
    order = nH

    # model_name = f"{file_name}_FC" if FC else f"{file_name}_vibronic"
    model_name = f"{file_name}"

    project.log_conf.setLevelDebug()
    # ----------------------------------------------------------------
    print("We are running calculation for {:} model!".format(file_name))

    # read in model parameters
    if use_JSON_flag:
        path = join(root,f'model_{model_name}.json')
        model = get_model_from_json_file(path, order)

    else:
        breakpoint()
        path = join("", 'model.op')
        model = get_model_from_op_file(path, order)

    # run CC code
    output_path_ABS, output_path_ECD = generate_acf_data(model, model_name, order, t_final, nof_steps=int(1e4))
    print(output_path_ABS)
    # interpolate for ACF(ABS)
    print("-"*40 + "\nInterpolating ABS\n" + "-"*40 + "\n")

    normalized_path_ABS = project.spectra.generate_normalized_acf_results(
            dirname(output_path_ABS),
            basename(output_path_ABS),
            None,
            mctdh_t_final=t_final*0.5,
            mctdh_dt=0.1
        )

    # interpolate for ACF(ECD)
    # print("-"*40 + "\nInterpolating ECD\n" + "-"*40 + "\n")
    # normalized_path_ECD = project.spectra.generate_normalized_acf_results(
    #         dirname(output_path_ECD),
    #         basename(output_path_ECD),
    #         None,
    #         mctdh_t_final=t_final*0.5,
    #         mctdh_dt=0.1
    #     )

    if (MCTDH_installed_locally := False):
        print('Do you want to plot the ABS spectra? Press c to continue.')
        breakpoint()

        # plot spectra
        print("-"*40 + "\nPlotting Spectrum\n" + "-"*40 + "\n")
        gnuplot_spectrum(
             f"{model_name}_{order_dict[order]}_tf{int(t_final):}",
             basename(normalized_path_ABS),
             f"{model_name}_{order_dict[order]}",
             order,
             t_final,
             FC,
         )

        os.system("gnuplot spectrum_plotting.pl")

        write_acf_plotting_file(output_path_ABS, normalized_path_ABS, FC, int(t_final))
        os.system("gnuplot acf_plotting.pl")