import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
    
from test_sc2metric import *
from test_bases_created_plugin import *
from test_resource_tracker_plugin import *

if __name__ == '__main__':
    unittest.main()
