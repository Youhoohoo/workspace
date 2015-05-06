#!/usr/bin/python2.7
#coding=utf-8
"""
 this file stores the common configurations
"""

# local host
LOCALHOST='127.0.0.1'

# socket server port 
SOCKET_SERVER_PORT_START = 21567

# socket buffer size
SOCKET_BUFF_SIZE = 1024

# max connection for each server
SOCKET_MAX_CONNECTION_NUM = 3

# rpc
RPC_HOST = 'localhost'
RPC_ROUTING_KEY = 'simulation_rpc_queue'

DEBUG_MODE = True

if DEBUG_MODE:
    import os
    RPC_ROUTING_KEY += '_' + os.environ['USER']
