import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
    
import metrics

import test_sc2metric
from test_sc2metric import *

import test_bases_created_plugin
from test_bases_created_plugin import *

if __name__ == '__main__':
    unittest.main()
