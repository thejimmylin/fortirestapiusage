"""
This file is used for importing all the fortirestapiusage things, so other .py file in
samples could import them from here.
"""
import os
import sys
repo_root = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
sys.path.insert(1, repo_root)

from fortirestapiusage.clients import *  # NOQA
