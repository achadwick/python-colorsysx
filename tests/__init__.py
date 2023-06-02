"""Test shim.

Importing this allows pytest to find the source tree's main module.

"""

# Imports and sys.path manipulations::

from os.path import dirname
from os.path import samefile
from os.path import abspath
import sys


tests_dir = abspath(dirname(__file__))
parent_dir = dirname(tests_dir)

assert samefile(sys.path[0], parent_dir)
