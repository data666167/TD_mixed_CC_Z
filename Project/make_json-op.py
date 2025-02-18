""" Module Description

Manually initialize some Hamiltonians.
Also support some helper functions.

"""

# system imports
import sys
import os
from os.path import join,abspath,dirname

# third party imports
import numpy as np
import parse  # used for loading data files


# Get the current working directory
current_working_directory = os.getcwd()

# Calculate the absolute path to the 'project' directory
project_path = abspath(join(dirname(__file__), '..'))

# Add the parent directory to sys.path
#sys.path.append(project_path)
sys.path.insert(0, project_path)
from project.vibronic import vIO, VMK

file_paths = os.path.join(project_path,'src_model')
print(os.listdir(file_paths))

for file_op in os.listdir(file_paths):
    try:
        json_file_name = file_op.replace('.op','.json')
        model = vIO.extract_excited_state_model_op(f'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/src_model/{file_op}')
        vIO.save_model_to_JSON(f'../src_json/{json_file_name}', model)
    except:
        print('\n')
        print(json_file_name)
        print('\n')
    
    
    

# removes fictitious surface 
# model = vIO.extract_excited_state_model_op('/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/h2o_vibronic_linear.op')
# vIO.save_model_to_JSON('./t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/h2o_vibronic_linear.json', model)