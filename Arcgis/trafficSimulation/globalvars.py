#!/usr/bin/python2.7
#coding=utf-8

"""globals.py
This file stores some global variables that will
be used in this project.
"""

import os
import sys

# db handler
this_file_path = os.path.realpath(__file__)
this_file_path_dir = os.path.split( this_file_path )[0]
sys.path.insert(0, os.path.join(this_file_path_dir, 'db'))
import DBHelper
dbhelper = DBHelper.DBHelper()
sys.path.remove( sys.path[0] )

