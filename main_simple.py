# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1, 2, 3, 4" 
from main_simple_lib import *

im = load_image('examples/v_whJ6ESGNoyY_11_combined.jpg')
query = 'If a person wanted to give one of the dogs to the other person to walk, would he be able to do so easily?'

show_single_image(im)
code = get_code(query)

execute_code(code, im, show_intermediate_steps=True)