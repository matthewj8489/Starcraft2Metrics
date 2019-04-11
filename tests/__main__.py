import os
import sys

#if __name__ == '__main__':
#    sys.path.insert(0, os.path.abspath("..\\"))

import inspect

if __name__ == '__main__':
    filename = os.path.abspath(inspect.getfile(inspect.currentframe()))
    thispath = os.path.dirname(filename)
    normpath = os.path.normpath(os.path.join(thispath, os.pardir))
    sys.path.insert(0, normpath)

    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
    
import metrics    
import test_plugins
import test_sc2metric
import test_bases_created_plugin
from test_plugins import TestPlugins
from test_sc2metric import TestMetrics
from test_bases_created_plugin import TestBasesCreatedPlugin

if __name__ == '__main__':
    unittest.main()
