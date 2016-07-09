import sys
'''
>>> sys.modules is a dictionary containing all the modules that have ever been imported
    since Python was started;
>>> 'the key'   is 'the module name'
>>> 'the value' is 'the module object'
'''
print '\n'.join( sys.modules.keys() )

from fileinfo2 import MP3FileInfo
'''
>>> Every Python class has a buit-in class attribute __module__,
>>> which is the 'name of the module' in which the class is defined
>>> Combining this with the sys.modules dictionary, you can 'get a reference' to the module
    in which a class is defined
'''
module_name =  MP3FileInfo.__module__ 
module =  sys.modules[module_name]
print module
tm = module.testModule()
