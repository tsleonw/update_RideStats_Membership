"""
Created on Sat Jan 29 11:37:44 2022

@author: Leon Webster

© 2022, RideStats, LLC.

This file allows tests to be run from a separate test directory
"""

__version__ = '1.0.0'

import pathlib
import sys
# This line is neccessary for test code to find files
sys.path.append(str(pathlib.Path(__file__).parent))
