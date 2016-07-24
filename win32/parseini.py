from ConfigParser import ConfigParser

# instantiate
config = ConfigParser()

# parse existing file
config.read('sample.ini')

# read values from a section
mystring = config.get('section_a','string_val')
mybool = config.get('section_a','bool_val')
myint = config.get('section_a','int_val')
mypi = config.get('section_a','pi_val')

# update existing value
config.set('section_a','string_val','hello world')

# add a new section and some values
config.add_section('section_b')
config.set('section_b', 'not_found_val',404)
config.set('section_b', 'mean_val','spam')

# write our config to the file sample.out
with open('sample.out','wb') as configfile:
    config.write(configfile)
