import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath("..\\"))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
    
    
import test_plugins
import test_sc2metric
from test_plugins import TestPlugins
from test_sc2metric import TestMetrics

if __name__ == '__main__':
    unittest.main()
