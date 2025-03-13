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

def generate_acf_data(model, file_name, order, t_final=10.0, nof_steps=int(1e4), FC=False, compare_FCI=False):
    """ x """

    # initalize object 
    hamiltonian = vibronic_hamiltonian(
        model, file_name,
        hamiltonian_truncation_order=order, cc_truncation_order=order,
        T_truncation_order=1, Z_truncation_order=nZ,
        calculate_population_flag=False,
    )
    
    # Call integration on object 
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

def generate_acf_data_oz(model, file_name, order, t_final=10.0, nof_steps=int(1e4), FC=False, compare_FCI=False):
    """ x """

    # initalize object 
    hamiltonian = vibronic_hamiltonian(
        model, file_name,
        hamiltonian_truncation_order=order, cc_truncation_order=order,
        T_truncation_order=1, Z_truncation_order=nZ,
        calculate_population_flag=False,
    )
    
    # Call integration on object 
    start_time = time.time()
    hamiltonian.rk45_integration_oz(t_final=t_final, nof_points=nof_steps)
    end_time = time.time()
    print(f"Very simple timing:   {end_time - start_time:10.4f}")

    # make plot and store data
    output_path = hamiltonian.save_acf_data(file_name=file_name, output_path=root_directory)
    hamiltonian.plot_acf(file_name=file_name, output_path=root_directory)

     
    file_path_ABS = join(root_directory,f"Norm{file_name}.txt")
    hamiltonian._save_data(file_path_ABS, hamiltonian.t_cc, hamiltonian.Norm_cc[:,0])

    return output_path


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


# run cmds
if (__name__ == '__main__'):
    neil =  False
    oz = True
    
    use_JSON_flag = True
    FC = False

    t_final = float(ntf)
    order = nH

    model_name = f"{file_name}"

    project.log_conf.setLevelDebug()
    # ----------------------------------------------------------------
    print("We are running calculation for {:} model!".format(file_name))

    # read in model parameters
    if use_JSON_flag:
        path = join(root,f'model_{model_name}.json')
        model = get_model_from_json_file(path, order)

    # run CC code
    if neil == True:
        output_path_ABS, output_path_ECD = generate_acf_data(model, model_name, order, t_final, nof_steps=int(1e4))
        print('output_path_ABS',output_path_ABS)
    
    # test my CC code 
    if oz== True:
        output_path_ABS, output_path_ECD = generate_acf_data_oz(model, model_name, order, t_final, nof_steps=int(1e4))
        print('output_path_ABS',output_path_ABS)
    
    # interpolate for ACF(ABS)
    print("-"*40 + "\nInterpolating ABS\n" + "-"*40 + "\n")

    normalized_path_ABS = project.spectra.generate_normalized_acf_results(
            dirname(output_path_ABS),
            basename(output_path_ABS),
            None,
            mctdh_t_final=t_final*0.5,
            mctdh_dt=0.1
        )

