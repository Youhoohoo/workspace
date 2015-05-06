#!/usr/bin/python2.7
#coding=utf-8
"""
gen_monitors.py
This file generates a big set of monitors infomation randomly.
"""

import os
import sys
import random
import json

class GenMonitor:
    """
    class name: GenMonitor,
        to generate a set of monitors.
    """
    def __init__(self, total_num=100):
        """
        function name: __init__,
            a initial function.
        input: None,
        output: None.
        """
        self.total_num = total_num
        self.monitors = []

    def fill_monitors(self):
        """
        function name: fill_monitors_infomation
        input: None,
        output: None.
        """
        for i in range(0 , self.total_num):
            info_rid = str(300000 + i)
            info_name = "卡口_" + str(i+1)
            info_desc_localid = "cam_" + info_rid
            lng = round(random.uniform(3,54),3)
            lat = round(random.uniform(73,136),3)
            info_geo = str(lng) + "," + str(lat)
            info = {
                "rid": info_rid,
                "check": "",
                "name": info_name,
                "tags": ["视频","摄像头","卡口"],
                "description": {
                                "localid": info_desc_localid,
                                "localaddr": "192.168.111.240",
                                "geo": info_geo,
                                "height": "1",
                                "gateway": "192.168.119.254", 
                                "description": "camera", 
                                "manufacturer": "iie.iie",
                                "name": "卡口视频",
                                "birthdate": "201308",
                                "#text": "",
                                "streamurl": "rtmp://192.168.119.193/live/stream111240",
                                "localport": "7000"
                                },
                "properties": {
                                "photo": {
                                        "name": "photo",
                                        "direction": "RES_2_USER",
                                        "type": {
                                                        "name": "data",
                                                        "org": "iie"
                                                        },
                            		"description": {
                                                	"comment": "taking photos of cars"
                                                	},
                                	"dynamic": False
                                        }
                                }, 
                "relationship": {
                                }, 
                "lastModified": "2014-04-22 14:32:54"
        }
            data = json.dumps(info,sort_keys=True,ensure_ascii=False,indent=4)
            self.monitors.append(data)

    def write(self):
        """
        function name: write
        input: None,
        output: None.
        """

	this_file_path = os.path.realpath(__file__)
	this_file_dir_path = os.path.split(this_file_path)[0]
	
	writefile0 = open('./idmap.ini','w')
	for i in range(0, len(self.monitors)):
		value = str(300000+i)
		cam = '#cam_' + value + '=' +value + '\n'
		writefile0.write(cam)
	writefile0.close()

	os.mkdir(os.path.join(this_file_dir_path,'resource'))

        for i in range(0, len(self.monitors)):
		name = 'resource/'+'cam_'+str(300000+i)+'.json';
		filename = os.path.join(this_file_dir_path, name)
		print filename
        	writefile = open(filename, 'w')
		writefile.write(str(self.monitors[i]))
		writefile.close()

def __main__():
    genmonitor = GenMonitor(100)
    genmonitor.fill_monitors()
    genmonitor.write()


if __name__ == '__main__':
    __main__()

