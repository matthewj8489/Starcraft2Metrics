import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
    
from test_sc2metric import *
from plugins.test_bases_created_plugin import *
from plugins.test_resource_tracker_plugin import *
from plugins.test_apm_tracker_plugin import *
from test_util import *
from test_bod import *
from metric_factory.test_spawningtool_factory import *
from metric_factory.test_sc2reader_factory import *

if __name__ == '__main__':
    unittest.main()
