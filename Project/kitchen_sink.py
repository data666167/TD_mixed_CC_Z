# this file runs when called from terminal in the directory the file is stored and relies on the jan 30 directory setup
# this file when run will run both the mcdth calc and cc calc in respect both softwares 
# This file is run: python3 kitchen_sink.py model_{name}.op {time} 
# system imports
import sys
import os
from os.path import join,abspath,dirname
import subprocess

# third party imports
import numpy as np
import parse  # used for loading data files

# Get the current working directory
cwd = os.getcwd()

def main():
    # Extract arguments from sys.argv
    model_name = sys.argv[1]   
    time = sys.argv[2]
    cluster_rank = 2
    hamiltonian_rank = sys.argv[3]
    
    
    # runs command for test clean
    
    # prepare model name remove 'model_' and '.op'
    cc_model_name = model_name.replace('model_','')
    cc_model_name = cc_model_name.replace('.op','')
    print(f'{cluster_rank}',f'{hamiltonian_rank}',f'{time}',f'{cc_model_name}')

    subprocess.run(['python3','test_clean.py',f'{cluster_rank}',f'{hamiltonian_rank}',f'{time}',f'{cc_model_name}'])
    
    # runs command for mctdh 
    # change model op in h2o inp file
    mcdth_folder_name = model_name.replace('.op','')
    with open(join(cwd,'h2o.inp'), 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        lines[2] = f'name = {mcdth_folder_name} \n'
        lines[12] = f'opname = {mcdth_folder_name} \n'
        lines[6] = f'tfinal = {int(time)/2} tout = 0.1 \n'   
        file.seek(0)
        file.writelines(lines)
    
    subprocess.run(['mctdh86','-mnd','-w','h2o.inp'])

    # runs autospec commands for normalized data - from test clean
    # find autospec cc file
    normalized_cc_data =f'ACF_ABS_CC_{cc_model_name}_normalized.txt'
    print(normalized_cc_data.replace('.txt','.pl'))
    # runs autospec commands 
    subprocess.run(['autospec86','-o',normalized_cc_data.replace('.txt','.pl'),'-f',normalized_cc_data,'-p','8000','20','0','ev','30','1'])
    
    # run file
    subprocess.run(['autospec86','-o',f'{mcdth_folder_name}.pl','-f',f'./{mcdth_folder_name}/auto','-p','8000','20','0','ev','30','1'])
        
     
    # edits acf plotting file 
    with open(join(cwd,'acf_plotting.pl'), 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        lines[2] = "set output \'{}\' \n".format(join(cwd, mcdth_folder_name + '_acf.png'))
        lines[9] = "plot \'{}\' using 1:2 with lines ls 2 lc \'black\' title \'MCTDH\', \\\n".format(join(cwd,mcdth_folder_name,'auto'))
        lines[10] = "\'{}\' using 1:2 with lines ls 2 lc \'red\' title \'CC\' \n".format(join(cwd,normalized_cc_data))
        file.seek(0)
        file.writelines(lines)

    # edits spectra plotting file
    with open(join(cwd,'spectrum_plotting.pl'), 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        lines[2] = "set output \'{}\' \n".format(join(cwd,mcdth_folder_name+'_spectrum.png'))
        lines[9] = "plot \'{}\' using 1:2 with lines ls 2 lc \'black\' title \'MCTDH\', \\\n".format(join(cwd,mcdth_folder_name+'.pl'))
        lines[10] = "\'{}\' using 1:2 with lines ls 2 lc \'red' title \'CC\' \n".format(join(cwd,normalized_cc_data.replace('.txt','.pl')))
        file.seek(0)
        
        file.writelines(lines)
    # run graph commands 
    subprocess.run(['gnuplot','acf_plotting.pl'])
    subprocess.run(['gnuplot','spectrum_plotting.pl']) 
    
if (__name__ =='__main__'):
    main()
