from main_simple_lib import *

im = load_image('https://viper.cs.columbia.edu/static/images/kids_muffins.jpg')
query = 'How many muffins can each kid have for it to be fair?'

show_single_image(im)
code = get_code(query)

execute_code(code, im, show_intermediate_steps=True)