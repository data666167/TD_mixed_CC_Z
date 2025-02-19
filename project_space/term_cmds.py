import os 
import re

def replace(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()

# model_names = ['model_h2o_H1','model_h2o_H2','model_h2o_H3','model_h2o_H4','model_h2o_H2_S1_Z1']

# for idx, model_name in enumerate(model_names):
#     replace('h2o_S1.inp',model_names[idx-1],model_name)
#     os.system('mctdh86 -mnd -w h2o_S1.inp')
#     os.system(f'autospec86 -o {model_name}.pl -f {model_name}/auto -p 8000 30 10 ev 30 1')
#     replace('spectrum_plotting.pl',f'\'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/{model_names[idx-1]}.png\'',f'\'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/{model_name}.png\'')
#     replace('spectrum_plotting.pl',f'\'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/{model_names[idx-1]}.pl\'',f'\'/home/oz_computron/Desktop/Research_idea/mixed_reprsentation/t-amplitudes-8171b20377162cf3b704c0d83f7eeae58bcbfdb5/{model_name}.pl\'')
#     os.system('gnuplot spectrum_plotting.pl')
os.system()