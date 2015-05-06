#!/usr/bin/python2.7
#coding=utf-8

"""DBoperation.py
This file defines a set of db operations
"""

import sys
import traceback
import os

this_file_path = os.path.realpath(__file__)
this_file_path_dir = os.path.split(this_file_path)[0]
sys.path.insert( 0 , os.path.join(this_file_path_dir , '..' ) )
import globalvars
sys.path.remove( sys.path[0] )

import DBconfig

def fetch_init_cars_general():
    """
    function name: fetch_init_cars_general
        to fetch the general info from the init car collection from the mongo db.
    """
    db = globalvars.dbhelper.getDB()   # the db handler
    try:
        solutions = db[DBconfig.DATA_BASE][DBconfig.Collection_initcars].find()
        res = []
        for each_solution in solutions:
            res.append( {'solution_id'  : each_solution['solution_id'] ,
                         'solution_name': each_solution['solution_name'] ,
                         'description'  : each_solution['description'] ,
                         'car_num'      : each_solution['car_num']
                         })
        return res
    except:
        traceback.print_exc()
        return []

def fetch_init_cars_detail(solution_id = 1):
    """
    function name : fetch_init_cars_detail
        according the init_cars_solution.track{car_id} to read the db.cars
        and list the cars_detial
    """
    db = globalvars.dbhelper.getDB() #the db handler
    try:
        all_solutions = db[DBconfig.DATA_BASE][DBconfig.Collection_initcars].\
            find({'solution_id':solution_id})
        for each_solution in all_solutions:
            tracks = each_solution['tracks'] # get one track in db[init_cars]
            res = []
            for each_track in tracks:
                car_id = each_track['car_id'] # get car_id in db[init_cars][tracks]
                track_id = each_track['track_id'] # get tracks_id in db[init_cars][tracks] 
                # use car_id find the mate one in db[cars]   
                one_car = db[DBconfig.DATA_BASE][DBconfig.Collection_cars].\
                    find_one({'car_id':car_id})
                # use tracks_id find the mate one in db[tracks]           
                one_track = db[DBconfig.DATA_BASE][DBconfig.Collection_tracks].\
                    find_one({'track_id':track_id})
                # get the start_segment_id in db[tracks][start_segment]
                one_start_segment_id = one_track['start_segment']['segment_id']
                # get the start direction in db[tracks][start_segment]
                one_start_direction = one_track['start_segment']['direction']
                # get the road percent in db[tracks][start_segment]
                start_p = one_track['start_segment']['percent']
                if one_start_direction != 1:
                    start_p = 1.0 - start_p
                p = start_p
                # use one_start_segment_id find the mate one_segment in db[segments]                    
                one_segment = db[DBconfig.DATA_BASE][DBconfig.Collection_segments].\
                    find_one({'segment_id':one_start_segment_id})
                # get one_point1_id in db[segments]
                one_point1_id = one_segment['point1_id'] 
                # use one_point1_id find the mate ponit1 in db[points]
                point1 = db[DBconfig.DATA_BASE][DBconfig.Collection_points].\
                    find_one({'point_id':one_point1_id})
                # get x1 and y1 in db[points]
                x1 = point1['x']
                y1 = point1['y']
                one_point2_id = one_segment['point2_id']
                point2 = db[DBconfig.DATA_BASE][DBconfig.Collection_points].\
                    find_one({'point_id':one_point2_id})
                x2 = point2['x']
                y2 = point2['y']
                # calculate the start_point_x and start_point_y
                start_point_x = p * x2 + (1 - p) * x1 
                start_point_y = p * y2 + (1 - p) * y1
                res.append({
                    'car_id'        : car_id ,
                    'car_color'     : one_car['car_color'] ,
                    'car_type'      : one_car['car_type'] ,
                    'max_speed'     : one_car['max_speed'] ,
                    'start_point_x' : start_point_x ,
                    'start_point_y' : start_point_y ,
                    'tracks'        : one_track # not handle data
                })
            return res
    except:
        traceback.print_exc()
        return []

def fetch_monitors():
    """
    function name : fetch_monitors
        to read monitors information in db.monitors
    input: None,
    output: a list of monitors to be revealed on the map.
        NOTE that the info contains the x, y coordinates.
    """

    db = globalvars.dbhelper.getDB() #the db handler
    try:
        all_monitors = db[DBconfig.DATA_BASE][DBconfig.Collection_monitors].find()
        res = []
        for each_monitor in all_monitors:
            segment_id = each_monitor['segment_id'] # get one segment_id in db[monitors]
            # use segment_id find the mate one in db[segments]           
            one_segment = db[DBconfig.DATA_BASE][DBconfig.Collection_segments].\
                find_one({'segment_id':segment_id})
            # get the ponit_id in db[segments]
            one_point_id = one_segment['point1_id']
            # use one_point_id find the mate one_point in db[points]                    
            one_point1 = db[DBconfig.DATA_BASE][DBconfig.Collection_points].\
                find_one({'point_id':one_point_id})
            x = one_point1['x']
            y = one_point1['y']
            res.append({
                'monitor_id'    : each_monitor['monitor_id'] ,
                'segment_id'    : segment_id ,
                'x'             : one_point1['x'] ,
                'y'             : one_point1['y'] ,
                'percent'       : 0 ,
                'direction'     : 1
                })
        return res
    except:
        traceback.print_exc()
        return []

def fetch_monitor_info():
    """
    function name : fetch_monitor_info
        to read monitors information in db.monitors
    """

    db = globalvars.dbhelper.getDB() #the db handler
    try:
        all_monitors = db[DBconfig.DATA_BASE][DBconfig.Collection_monitors].find()
        res = []
        for each_monitor in all_monitors:
            segment_id = each_monitor['segment_id'] # get one segment_id in db[monitors]
            res.append({
                'monitor_id'    : each_monitor['monitor_id'] ,
                'segment_id'    : segment_id 
                })
        return res
    except:
        traceback.print_exc()
        return []



def fetch_records(monitor_id):
    """
    function name : fetch_records
        to get the car pass the monitors information
    input: monitor_id, an integer indicating the target monitor id
    output: a list of {'car_id':..., 'time':...}
    """

    db = globalvars.dbhelper.getDB()

    try:
        monitor_id = int(monitor_id)
        all_records = db[DBconfig.DATA_BASE][DBconfig.Collection_monitor_records].\
            find_one({'monitor_id': monitor_id})
        record = all_records['record']
        return record
    except:
        traceback.print_exc()
        return []

def fetch_solution_info(solution_id):
    """
    function name: fetch_solution_info
        according the front solution_id get the solutions from the mongo db.
    input: solution_id. 
    output: None
    """
    db = globalvars.dbhelper.getDB()   # the db handler
    try:
        solution = db[DBconfig.DATA_BASE][DBconfig.Collection_initcars].\
            find_one({'solution_id' : solution_id})
        res = []
        res.append( {'solution_id'  : solution['solution_id'] ,
                     'solution_name': solution['solution_name'] ,
                     'description'  : solution['description'] ,
                     'car_num'      : solution['car_num']
        })
        return res
    except:
        traceback.print_exc()
        return []

def verify(user_name, user_password):
    """
    function name : verify
        verify teh  user_name and user_password in mongo db.
    input:user_name and user_password
    output:None
    """
    db = globalvars.dbhelper.getDB()
    try:
        user = db[DBconfig.DATA_BASE][DBconfig.Collection_users].\
            find_one({'user_name' : user_name})
        if str(user_name) == str(user['user_name']) and str(user_password) == str(user['user_password']):
            return user['user_id']
        else:
            return -1
    except:
        traceback.print_exc()
        return -1

def store_records(records):
    db = globalvars.dbhelper.getDB()
    try:
        monitor_record = db[DBconfig.DATA_BASE][DBconfig.Collection_monitor_records]
        for each_record in records:
            monitor_id = each_record['monitor_id']
            target_record = monitor_record.find_one({'monitor_id': monitor_id})
            target_record['record'].extend(each_record['record'])
            monitor_record.save(target_record)
    except:
        traceback.print_exc()

def __unit_test_fetch_init_cars_general():
    fetch_init_cars_general()
    fetch_init_cars_detail()
    fetch_monitors()
    fetch_monitor_info()
    fetch_solution_info(1)
    verify(user_name, user_password)
    """
    records = [
        {
        'monitor_id': 0,
        'record': [
            {
            'car_id': 88,
            'time': '888',
            },
            {
            'car_id':99,
            'time': '999',
            }
        ]
        },
        {
        'monitor_id': 1,
        'record': [
            {
            'car_id': 88,
            'time': '888',
            },
            {
            'car_id':99,
            'time': '999',
            }
        ]
        },
    ]
    """
    store_records(records)
    all_records = fetch_records(0)

if __name__ == '__main__':
    __unit_test_fetch_init_cars_general()
