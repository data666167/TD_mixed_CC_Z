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

# -------------------------------------------------------------------------------------------------


def print_elements_of_shape(shape):
    print("Template shape\n")
    for k, v in shape.items():
        print(k, v)
    print('\n')


def print_element_types_of_model(model):
    for k, v in model.items():
        if isinstance(v, np.ndarray):
            print(k, v.shape)
        else:
            print(k, v)
    print('\n')


# -------------------------------------------------------------------------------------------------
def generate_fake_model_values(model):
    """ Fill linear hamiltonian with semi random values """
    A, N = model[VMK.A], model[VMK.N]

    model[VMK.w] = np.linspace(0.1, 0.2, num=N, endpoint=True, dtype=np.float64)
    model[VMK.w] -= np.random.uniorm(low=0.001, high=0.002, size=N)
    model[VMK.E] = np.random.uniform(0.05, 0.1, model[VMK.E].shape)
   # force the energy to be symmetric
    model[VMK.E] = np.tril(model[VMK.E]) + np.tril(model[VMK.E], k=-1).T

    for a in range(A):  # make the diagonal slightly larger
        model[VMK.E][a, a] += 2

    model[VMK.etdm].fill(complex(0.1))
    model[VMK.mtdm].fill(complex(0.1))

    disp = 0.004 / model[VMK.w]
    for i in range(N):
        # force the linear terms to be symmetric
        upTri = np.random.uniform(-disp[i], disp[i], model[VMK.E].shape)
        model[VMK.G1][i, ...] = np.tril(upTri) + np.tril(upTri, k=-1).T

    return


# -------------------------------------------------------------------------------------------------
def simple_template_1x1_model(A, N, order=0):

    # example shape of tensors
    shape = vIO.model_shape_dict(A, N)
    print_elements_of_shape(shape)

    model = vIO.model_zeros_template_json_dict(A, N, highest_order=order)
    print(f"Example {order=} model\n")
    print_element_types_of_model(model)

    # make fake values
    generate_fake_model_values(model)

    return model


# -------------------------------------------------------------------------------------------------


def make_model_one():
    """ Create a Hamiltonian that is ...
    This can be called by the example_script.py
    Basically
    1 electronic surface
    3 normal modes
    1st order (linear) truncation
    """
    A, N, H_order = 1, 3, 4
    model = vIO.model_zeros_template_json_dict(A, N, highest_order=H_order)

    # fill in predetermined values
    model[VMK.E][0, 0] = 10
    model[VMK.w][:] = np.linspace(0,3,N)
    # Implement beta as the as a predetermined value for each mode  
    # this needs to be implemented in VMK 
    beta = [0.1,0.2,0.4]
    # model[VMK.w][:] = 0.1

    model[VMK.etdm].fill(complex(0.1))
    model[VMK.mtdm].fill(complex(0.1))
   
    if H_order >= 1:  # fill linear terms
        model[VMK.G1][0, ...].fill(0.1)# [0.1, 0.2, 0.3, ]
        model[VMK.G1][1, ...].fill(0.2) #= [0.1, 0.2, 0.3, ]
        model[VMK.G1][2, ...].fill(0.3) #= [0.1, 0.2, 0.3, ]
    
    if H_order >= 2:  # fill quadratic terms
        model[VMK.G2][1, 0, ...].fill(0.1) #= [0.1, 0.2, 0.3, ]
        model[VMK.G2][0, 1, ...].fill(0.1) #= [0.1, 0.2, 0.3, ]
        # will need to symmetrize after filling with values
        
    if H_order >= 4:  # fill quartic terms
        model[VMK.G4].fill(0.1) #= [0.1, 0.2, 0.3, ]
        for i in range(N):
            model[VMK.G4][i,i,i,i,...].fill(beta[i]) 
            
       # model[VMK.G4][1, 0, 0, 0, ...].fill(0.1) #= [0.1, 0.2, 0.3, ]
        # will need to symmetrize after filling with values
    
    
    return model,H_order

#----------------------------------------------------------------
def make_model_one():
    """ Create a Hamiltonian that is ...
    This can be called by the example_script.py
    Basically
    1 electronic surface
    3 normal modes'{root_directory}/test_auto.pl' using 1:3 with lines ls 1 lc 'black' title 'MCTDH',",
        f"
    1st order (linear) truncation
    """
    A, N, H_order = 1, 3, 2
    model = vIO.model_zeros_template_json_dict(A, N, highest_order=H_order)

    # fill in predetermined values
    model[VMK.E][0, 0] = 14
    model[VMK.w][:] = [1,2,3]#np.linspace(0,3,N)
    # Implement beta as the as a predetermined value for each mode  
    # this needs to be implemented in VMK 
    beta = [0.1,0.2,0.4]
    # model[VMK.w][:] = 0.1

    model[VMK.etdm].fill(complex(0.1))
    model[VMK.mtdm].fill(complex(0.1))
   
    if H_order >= 1:  # fill linear terms
        model[VMK.G1][0, ...].fill(0.1)# [0.1, 0.2, 0.3, ]
        model[VMK.G1][1, ...].fill(0.2) #= [0.1, 0.2, 0.3, ]
        model[VMK.G1][2, ...].fill(0.3) #= [0.1, 0.2, 0.3, ]
    
    if H_order >= 2:  # fill quadratic terms
        model[VMK.G2][1, 0, ...].fill(0.1) #= [0.1, 0.2, 0.3, ]
        model[VMK.G2][0, 1, ...].fill(0.1) #= [0.1, 0.2, 0.3, ]
        # will need to symmetrize after filling with values
        
    if H_order >= 4:  # fill quartic terms
        model[VMK.G4].fill(0.1) #= [0.1, 0.2, 0.3, ]
        for i in range(N):
            model[VMK.G4][i,i,i,i,...].fill(beta[i]) 
        breakpoint()
       # model[VMK.G4][1, 0, 0, 0, ...].fill(0.1) #= [0.1, 0.2, 0.3, ]
        # will need to symmetrize after filling with values
    
    
    return model,H_order

user = True

#-------------------------------------------------------------------
# Test_H_0

def make_model_test(A,N,H_order):
    """ Create a Hamiltonian that is ...
    This can be called by the example_script.py
    Basically
    1 electronic surface
    3 normal modes'{root_directory}/test_auto.pl' using 1:3 with lines ls 1 lc 'black' title 'MCTDH',",
        f"
    1st order (linear) truncation
    """
    #A, N, H_order = 1, 3, 1
    model = vIO.model_zeros_template_json_dict(A, N, highest_order=max(H_order,1))

    # Fill in predetermined values
    
    # Vertical energy 
    model[VMK.E][0, 0] = 10
    model[VMK.w][:] = [.8,.5] 
    print('ZPE:',np.sum(model[VMK.w])/2,'eV')

    # Dipole moments 
    model[VMK.etdm].fill(complex(0.1))
    model[VMK.mtdm].fill(complex(0.1))

    # Number of modes linear no mode coupling
    if H_order >= 1:  # fill linear terms
        model[VMK.G1][0, ...].fill(.12)# [0.1, 0.2, 0.3, ]
        model[VMK.G1][1, ...].fill(.15) #= [0.1, 0.2, 0.3, ]
        # model[VMK.G1][2, ...].fill(.03) #= [0.1, 0.2, 0.3, ]

    # First term with mode coupling  
    if H_order >= 2:  # fill quadratic terms
        model[VMK.G2][0, 0, ...].fill(0.2) 
        model[VMK.G2][0, 1, ...].fill(0.3) 
        # model[VMK.G2][0, 2, ...].fill(0.3)        
        model[VMK.G2][1, 1, ...].fill(0.4) 
        # model[VMK.G2][1, 2, ...].fill(0.7) 
        # model[VMK.G2][2, 2, ...].fill(0.9)
        
        # lower triangular
        model[VMK.G2][1, 0, ...].fill(0.3) 
        # model[VMK.G2][2, 0, ...].fill(0.3)
        # model[VMK.G2][2, 1, ...].fill(0.7)
    
    # Fix these later  
    if H_order >= 3:
        model[VMK.G3][1, 0, ...].fill(0.05)

    
    if H_order >= 4:  # fill quartic terms
        #model[VMK.G4].fill(0.1) #= [0.1, 0.2, 0.3, ]
        for i in range(N):
            model[VMK.G4][i,i,i,i,...].fill(.1) 
       # model[VMK.G4][1, 0, 0, 0, ...].fill(.1) #= [0.1, 0.2, 0.3, ]
        # will need to symmetrize after fillig with values
    return model,H_order
#----------------------------------------------------------
def make_model_json(filename,A,N,H_order):
    """ Create a Hamiltonian that is ...
    Reads an op file and symmetrizes the hamiltonian
    """
    if f'{filename}'[-2:] != 'op':
        print('wrong file name') 
        raise Exception
    
    with open(f'{filename}',mode='r') as file:

        text = file.readlines() 
        for line in text:
            if line == 'PARAMETER-SECTION':
                print('pop')
                

    #A, N, H_order = 1, 3, 1
    model = vIO.model_zeros_template_json_dict(A, N, highest_order=max(H_order,1))

    # Fill in predetermined values
    
    # Vertical energy 
    model[VMK.E][0, 0] = 10
    model[VMK.w][:] = [.8,.5] 
    print('ZPE:',np.sum(model[VMK.w])/2,'eV')

    # Dipole moments 
    model[VMK.etdm].fill(complex(0.1))
    model[VMK.mtdm].fill(complex(0.1))

    # Number of modes linear no mode coupling
    if H_order >= 1:  # fill linear terms
        model[VMK.G1][0, ...].fill(.12)# [0.1, 0.2, 0.3, ]
        model[VMK.G1][1, ...].fill(.15) #= [0.1, 0.2, 0.3, ]
        # model[VMK.G1][2, ...].fill(.03) #= [0.1, 0.2, 0.3, ]

    # First term with mode coupling  
    if H_order >= 2:  # fill quadratic terms
        model[VMK.G2][0, 0, ...].fill(0.2) 
        model[VMK.G2][0, 1, ...].fill(0.3) 
        # model[VMK.G2][0, 2, ...].fill(0.3)        
        model[VMK.G2][1, 1, ...].fill(0.4) 
        # model[VMK.G2][1, 2, ...].fill(0.7) 
        # model[VMK.G2][2, 2, ...].fill(0.9)
        
        # lower triangular
        model[VMK.G2][1, 0, ...].fill(0.3) 
        # model[VMK.G2][2, 0, ...].fill(0.3)
        # model[VMK.G2][2, 1, ...].fill(0.7)
    
    # Fix these later  
    if H_order >= 3:
        model[VMK.G3][1, 0, ...].fill(0.05)

    
    if H_order >= 4:  # fill quartic terms
        #model[VMK.G4].fill(0.1) #= [0.1, 0.2, 0.3, ]
        for i in range(N):
            model[VMK.G4][i,i,i,i,...].fill(.1) 
       # model[VMK.G4][1, 0, 0, 0, ...].fill(.1) #= [0.1, 0.2, 0.3, ]
        # will need to symmetrize after fillig with values
    return model,H_order

#----------------------------------------------------------
def add_fake_surface(path, model):
    with open(path,'r') as fp:
        data = fp.read()
    
    assert '' in data, 'couldnt find x'
    data.replace('','')
    
    with open(path,'w') as fp:
        fp.write(data)

    return
    
        
A,N= 1,2
H_order = 2
# making a model op file for h_o fails talk to neil

workspace_root = join(project_path)
path = join(workspace_root,f'model_H{H_order}_A{A}_N{N}.json')
path_op = path.replace('.json', '.op')

vIO.create_coupling_from_op_file('./','/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/h2o_vibronic_linear.op')

model,h_order = make_model_test(A, N, H_order)

vIO.save_model_to_JSON(path, model)
# vIO.write_model_op_file(path_op, model,H_order)
# add_fake_surface(path_op,model)
# # optional
# loaded_model = vIO.load_model_from_JSON(path)
# print("-"*60)
# vIO.print_model_compact(loaded_model)


#------------------------------------------------------------------- Folders and files

