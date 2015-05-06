#!/usr/bin/python2.7
#coding=utf-8

"""DBHelper.py

The DB basis
"""

import pymongo
import sys
import os

# add in the DBconfig
this_file_path = os.path.realpath(__file__)
this_file_path_dir = os.path.split( this_file_path )[0]
sys.path.insert(0, this_file_path_dir)
import DBconfig
sys.path.remove( sys.path[0] )


class DBHelper:
    """
    class name: DBHelper
        the basic of db, containing the connecting, etc.
    """

    def __init__(self):
        self.__db_host = DBconfig.DB_HOST
        self.__db_port = DBconfig.DB_PORT
        # print self.__db_host, self.__db_port
        self.__db = None
    
    def getDB(self):
        if not self.__db:
            self.__db = pymongo.Connection(self.__db_host, self.__db_port)
        return self.__db


def __main__():
    dbhelper = DBHelper()
    print 'all data base names:', dbhelper.getDB().database_names()


if __name__ == '__main__':
    __main__()
