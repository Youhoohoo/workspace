#!/usr/bin/env python
#coding=utf-8

""" controller.py
This file is main center of the whole simulator
"""

import traceback
import os
import random
import sys
import json

# import db
this_file_path = os.path.realpath(__file__)
this_file_dir_path = os.path.split(this_file_path)[0]
sys.path.insert(0, os.path.join(this_file_dir_path, '../db'))
import DBoperation
sys.path.remove(sys.path[0])

#import simulator
sys.path.insert(0, os.path.join(this_file_dir_path, '../simulation'))
import simulator
one_simulator = simulator.Simulator()
sys.path.remove(sys.path[0])

class Controller:
    def __init__(self):
        pass
    def test_method(self, message_body):
        # message_body = message_body.upper()
        try:
            return message_body
        except:
            return ''

    def test_fetch_points(self, message_body):
        try:
            message_body = json.loads(message_body)
            points_num = int(message_body['num'])
            result = []
            upper_bound = 10
            lower_bound = 1
            for i in range(0, points_num):
                x = random.randint(lower_bound, upper_bound)
                y = random.randint(lower_bound, upper_bound)
                result.append( (x, y) )
            return result
        except:
            traceback.print_exc()
            return []

    def select_init_cars(self, message_body):
        """
        function name: select_init_cars,
            to select out a set of initial configurations and the 
            simulator will begin to set up.
        input: message_body,
            the arguments from the webserver, ie. the solution id.
        output: None
        """
        try:
            solution_id = int(message_body)
            all_car_dict = DBoperation.fetch_init_cars_detail(solution_id)
            print ' [*] the solution_id:', solution_id
            one_simulator.read_map()
            one_simulator.read_car_db(all_car_dict)

            all_monitors = DBoperation.fetch_monitor_info()
            one_simulator.read_monitor(all_monitors)

            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def select_conf(self, confs):
        """
        function name: the whole geteway for selecting a conf.
            This function will set up the configurations for cars, monitors, etc.
        input: confs
        output: SUCCESS or FAIL
        """
        try:
            confs = json.loads(confs)
            car_solution_id = int(confs['car_solution_id'])
            if not self.select_init_cars(car_solution_id):
                raise Exception("[*] select init car failed!")

            all_monitors_dict = DBoperation.fetch_monitors()
            monitors = []
            for each_monitor in all_monitors_dict:
                monitor_id = int(each_monitor['monitor_id'])
                x = float(each_monitor['x'])
                y = float(each_monitor['y'])
                monitors.append({'monitor_id' : monitor_id,
                                 'x'          : x, 
                                 'y'          : y
                                 })
		
            return {
                'result': 'SUCCESS',
                'monitors': monitors
            }
        except:
            traceback.print_exc()
            return {
                'result': 'FAIL',
                'monitors': []
            }
            

    def update_simulation(self, params):
        """
        function name: supdate_simulation,
            to get the situation of simulation in the future.
        input: params, 
            it is a string, produced by json.dumps.
            originally it is a dict type, containing the lefttop_x, lefttop_y,
            rightbottom_x, rightbottom_y, level, target_time
        output: a list of positions.
        """
        params = json.loads(params)

        res = []
        target_time = float(params['target_time'])
        lefttop_x = float(params['lefttop_x'])
        lefttop_y = float(params['lefttop_y'])
        rightbottom_x = float(params['rightbottom_x'])
        rightbottom_y = float(params['rightbottom_y'])
        level = int(params['level'])

        res,message = one_simulator.update_simulation(target_time, lefttop_x, lefttop_y,
            rightbottom_x, rightbottom_y, level)
        self.push_message(message)
        #res = one_simulator.update(target_time)
        return res

    #def push_message(self, records):
    #    for i in range(len(records)):
    #        print records[i]['monitor_id']

    def push_message(self,records):
        """
        function name: push_message,
            to push message to another server and work on simulator.py as a callback function
        input:records,
            they will be producted in simulator.py
        output:None
        """
        import re
        import time
        import base64
        import requests
           
        url = 'http://10.10.12.72:8080/data/update'
        image_file_path = u'/home/youjz/workplace/traffic_simulation_project_document/cars'

        for i in range(len(records)):
            monitor_id = records[i]['monitor_id']
            ttime = records[i]['record'][0]['time']
            timeArray = time.strptime(ttime,"%Y-%m-%d %H:%M:%S")
            timestamp = int(time.mktime(timeArray))
            info_name = '卡口_' + str(monitor_id)
            image_id = monitor_id % 100
            path = image_file_path + '/car_' + str(image_id) + '.jpg'
            image = open(path,'rb')
            mydata = image.read()
            data = base64.b64encode(mydata)
            data = {
                    "rid": str(300000+monitor_id),
                    "pid": "photo",
                    "data": data,
                    "timestamp": int( timestamp * 1000 )
                    }
            data = json.dumps(data)
            info = {
                "rid": str(300000+monitor_id),
                "pid": "photo",
                'data': data,
                "check": "e8dc4081b13434b45189a720b77b6818"
                }
            #params = json.dumps(info,sort_keys=True,ensure_ascii=False,indent=4)
            response = requests.post(url, data=info)
            print info_name + '消息发送成功'
            print '#'*10, response.text


if __name__=='__main__':
    records=[{
            'monitor_id': 1,
            'record': [{
                'car_id':25,
                'time': '2015-03-12 15:24:11'
                }]
                }]
    controller = Controller()
    controller.push_message(records)
