#!/usr/bin/env python
#coding=utf-8

""" callTable.py
This defines several rpc calls table.
"""

# key: the method name VISIBLE from webServer.
# value: the corresponding function of the simulator. THIS is the internal method.
call_table = {
    'test_method': 'test_method',
    'test_fetch_points': 'test_fetch_points',
    'select_conf': 'select_conf',
    'update_simulation': 'update_simulation',
}
