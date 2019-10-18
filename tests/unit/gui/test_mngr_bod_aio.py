import os
import sys

# relative paths for importing classes under test
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'gui')))

# unit test
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from unittest.mock import MagicMock
from unittest.mock import patch

# import gui
from gui.mngr_bod_aio import MngrBodAio

class TestMngrBodAio(unittest.TestCase):

    def test_(self):
        self.assertEqual(1, 0)

