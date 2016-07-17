''' Regression testing framework

This module will search for scripts in the same directory named XYZtest.py.
Each such script should be a test suite that tests a module through PyUnit.
(As of Python 2.1, PyUnit is included in the standard library as 'unittest')
This script will aggresgate all found test suits into one big test suits and
run them all at once.
'''
import os, sys, re, unittest

def regressionTest():
    path = os.path.abspath(os.path.dirname( sys.argv[0] ) )
    files = os.listdir(path)
    test = re.compile('test\.py$', re.IGNORECASE)
    files = filter(test.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = map(__import__, moduleNames)

    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite( map(load, modules) )

#   alltests = unittest.TestSuite()
#   for module in modules:
#       alltests.addTest(unittest.findTestCases(module) )
#   return alltests

if __name__ == '__main__':
    unittest.main( defaultTest='regressionTest')

