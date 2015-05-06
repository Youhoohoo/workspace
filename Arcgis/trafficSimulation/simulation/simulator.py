#!/usr/bin/python2.7
#coding=utf-8

'''
2015年4月21日19:20:30
重新整理simulator.py文件,精简掉所有调试所用代码。
'''

'''
2014年7月2日15:54:30
init()函数来读取in.txt文件中的所有点和边的信息并且随机生成指定数量的车
(生成了车的起点与终点),然后根据车的起点与终点生成车的路径保存在car.track中.
simulation(t)函数来返回所有车在t秒后的当前坐标(保存在一个列表中).
'''

import random
import time
import copy
import math
import os
import sys

this_file_path = os.path.realpath(__file__)
this_file_dir_path = os.path.split(this_file_path)[0]
sys.path.insert(0, os.path.join(this_file_dir_path, '../db'))
import DBoperation
sys.path.remove( sys.path[0] )

class Simulator:
    """
    class name: Simulator, the main class for simualting the whole 
    process.
    """
    #***************************全局数据************************************
    
    this_file_path = os.path.realpath(__file__)
    this_file_dir_path = os.path.split(this_file_path)[0]
    
    #点与边的所有信息所保存的文件路径
    point_road_filename = os.path.join(this_file_dir_path, 'in.txt')
    
    n = 0                                    #节点数 即point数
    m = 0                                    #边数 即road数
    car_num = 1000                           #需要模拟的车数量,目前为1,可以随时改成其他数,不影响运行
    Points = []                              #所有的节点
    Roads = []                               #所有的边(路)
    Cars = []                                #所有的车
    dict_road = {}                          #字典,从（start，end）到road_id 的字典,这个字典后面要用到
    monitor_sum = 0
    monitor_record = []
    monitor_id_list = []        # store all the monitors' id in this list
    
    #***************************全局数据************************************

    #***************************1.1读图************************************
    #读point与road的所有信息，完成全局变量Roads、Points的赋值
    def read_map(self):   
        f = open(self.point_road_filename)
        line = f.readline()
        result = []
        result = line.split('    ')
        n = int(result[0])
        m = int(result[1])
    
        for i in range(n):
            line = f.readline()
            result = []
            result = line.split('    ')
            point_id = int(result[0])
            x = float(result[1])
            y = float(result[2])
            new_point = point(x,y,point_id) #实例化一个point类
            self.Points.extend([new_point]) #将实例化的point加入全局变量Points当中
    
        for i in range(m):
            line = f.readline()
            result = []
            result = line.split('    ')
            road_id = int(result[0])
            road_start = int(result[1])
            road_end = int(result[2])
            road_length = float(result[3])
            new_road = road(road_id , road_start , road_end , road_length)
            self.Roads.extend([new_road])
    
        for i in self.Roads:
            self.dict_road[( i.start,i.end )] = i.id_r
            
        f.close()
        
        flag = 0
        Debug(flag , [len(self.Points) , ' ' , len(self.Roads)] )
        Debug(flag , [self.Points[len(self.Points)-1].x, ' ' , self.Points[len(self.Points)-1].y])
        Debug(flag , [self.Roads[len(self.Roads)-1].id_r , ' ' , self.Roads[len(self.Roads)-1].start , ' ' ,\
              self.Roads[len(self.Roads)-1].end , ' ' , self.Roads[len(self.Roads)-1].length ] )

    def read_monitor(self, l):  
    	#读卡口的所有信息，将monitor部署到相应的Roads上
        # l = fetch_monitor_info()
        # 数据类型应该类似 l = [{'monitor_id':'1','segment':1},{'monitor_id':'5','segment':2}...]
        self.monitor_sum = len(l)
        self.monitor_record  = [[] for i in range(self.monitor_sum) ]
        for i in range(len(l)):
            monitor_index = i # int(l[i]['monitor_id'])
            monitor_id = int(l[i]['monitor_id'])#读出l中的monitor_id信息
            segment_id = int(l[i]['segment_id'])#读出l中的segment_id信息

            self.Roads[segment_id].is_monitor = True#标定设置monitor的路段
            self.Roads[segment_id].monitor_id = monitor_id
            self.monitor_id_list.append( monitor_id )
            self.Roads[segment_id].monitor_index = monitor_index

    #生成车辆信息，完成全局变量Cars的赋值        
    def read_car_db(self, car_dict):
        self.Cars = []
        for one_car_dict in car_dict:
            car_obj = Car(one_car_dict)
            self.Cars.append(car_obj)

    #***************************2.1模拟车辆前进************************************
    def update_simulation(self, update_time_interval, lefttop_x=-10**10, lefttop_y=10*10, 
        rightbottom_x=10**10, rightbottom_y=-10*10, level=1):
        """
        function name: update_simulation, the update core.
            When called, it will update the cars' position. Also it will record the 
            cars passed the monitors.
        input: 
            update_time_interval, double type. The time interval of updating operation.
            lefttop_x, 
            lefttop_y,
            rightbottom_x,
            rightbottom_y,
                the position of the screen.
        output:
            a list of new car groups' position.
        """
        # update(update_time_interval)
        level = int(level)
        nrows, ncols = self.get_grids(level)
    
        res = []
    
        # deep copy
        for grid_i in range(0, nrows):
            res.append([])
            for grid_j in range(0, ncols):
                res[grid_i].append({
                    'x_total': 0,
                    'y_total': 0,
                    'density': 0,
                })
    
        x_step = (rightbottom_x - lefttop_x) / ncols
        y_step = (lefttop_y - rightbottom_y) / nrows
    
        update_time_interval = float(update_time_interval)
        for i in range(len(self.Cars)):
            # update the position of 
            self.get_new_car(update_time_interval, i)
            this_car_x = self.get_pos(i)[0]
            this_car_y = self.get_pos(i)[1]
    
            row_index = (lefttop_y - this_car_y) / y_step
            row_index = int(row_index)
    
            col_index = (this_car_x - lefttop_x) / x_step
            col_index = int(col_index)
            # print '#'*100, row_index, col_index, this_car_x, this_car_y, lefttop_x, lefttop_y, rightbottom_x, rightbottom_y
    
            # if beyond the viewport, then just ignore the car.
            if row_index <0 or col_index < 0 or row_index >= nrows or col_index >= ncols:
                continue
    
            # print 'before', res[row_index][col_index]['density']
            res[row_index][col_index]['x_total'] += this_car_x
            res[row_index][col_index]['y_total'] += this_car_y
            res[row_index][col_index]['density'] += 1
            # print 'after', res[row_index][col_index]['density']
        
        final_res = []
        for grid_i in range(0, nrows):
            for grid_j in range(0, ncols):
                if res[grid_i][grid_j]['density'] <= 0:
                    continue
                final_res.append({
                    'x': res[grid_i][grid_j]['x_total'] / res[grid_i][grid_j]['density'],
                    'y': res[grid_i][grid_j]['y_total'] / res[grid_i][grid_j]['density'],
                    'density': res[grid_i][grid_j]['density'],
                })
                
        moni_info = self.print_monitor_record()
        
        return final_res,moni_info

    def get_pos(self, i):
        '''
        由车辆编号i(即车在Cars中的编号，为了保持一致性，Cars[i].car_id=i)得出
        该车的当前位置（road_id,road_percent,dirc），得出该车的绝对坐标二元组
        （X,Y）
        '''
        per = self.Cars[i].road_percent
        if self.Cars[i].dirc == -1:
            per = 1.0 - per
        s = self.Roads[self.Cars[i].road_id].start
        e = self.Roads[self.Cars[i].road_id].end
        p = add( self.Points[s] , mul( sub(self.Points[e] , self.Points[s]) , per) )
        return (p.x , p.y)

    def get_new_car(self, t , i):
        '''
        更新第i辆车在t秒后的位置
        '''
        c = self.Cars[i]
        if len(c.track) == 0:
            c.done = True
            return
        path_length = c.v * t
        while path_length > 0:
            road_length = self.Roads[c.road_id].length   #车当前所在路的路长
            if c.track[0][2] == 1:                  #车在该路应该往正向走
                #print '车在该路应该往正向走'
                if len(c.track) == 1 :              #如果路径只剩下一个，则车在当前路的终点就是车的终点
                    end_per = (c.end)[1]          #车终点在路的正向百分比
                    if (c.end)[2] == -1:
                        end_per = 1.0 - end_per
                else :#路径不止一个，且车在当前路走正向，车在当前路的终点是
                      #当前路的终点
                    end_per = 1.0
                                         
                start_per = c.road_percent      #车当前位置在该路的正向百分比
                if c.dirc == -1:                #若车在当前路是反向
                    start_per = 1.0 - start_per
                    
                #卡口功能
                if self.Roads[c.track[0][0]].is_monitor == True and start_per == 0.0:#正向在卡口路上行驶,需要从起点0%位置出发才能算过了卡口
                    self.monitor_record[self.Roads[c.track[0][0]].monitor_index].append( {'time':str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) ),'car_id':i} )
                #卡口功能
                    
                if end_per * road_length <= start_per*road_length + path_length :
                    #车将开出当前路
                    #print '车将开出当前路'
                    #print 'path_length',path_length
                    #print 'start_per',start_per
                    #print 'end_per',end_per
                    path_length = start_per * road_length + path_length - \
                                  end_per * road_length
                    #print 'path_length',path_length
                    #print 'start_per',start_per
                    #print 'end_per',end_per
                    
                    c.track = (c.track)[1:]
                    if len( c.track ) > 0:        #车还有新的路要走
                        c.road_id = c.track[0][0]
                        c.road_percent = 0
                        c.dirc = c.track[0][2]
                    elif len( c.track ) == 0:   #车已经到终点
                        c.done = True
                        c.road_id = c.end[0]
                        c.road_percent = c.end[1]
                        c.dirc = c.end[2]
                        return
                else :  #车走不完当前路
                        #c.road_id 不变
                        #print '车走不完当前路'
                    c.road_percent = (start_per*road_length + path_length ) \
                                     / road_length
                    path_length = 0     #还能走路长归0
                    c.dirc = 1
                        
            elif c.track[0][2] == -1:       #车在该路应该往反向走
                #print '车在该路应该往反向走'
                if len(c.track) == 1 :      #如果路径只剩下一个，则车在当前路的终点就是车的起点
                    end_per = ( c.end )[1]  #车终点在路的逆向百分比
                    if (c.end)[2] == 1:
                        end_per = 1.0 - end_per
                else :                      #路径不止一个，且车在当前路走逆向，车在当前路的终点是
                    #当前路的终点
                    end_per = 1.0
                                        
                start_per = c.road_percent#车当前位置在该路的逆向百分比
                if c.dirc == 1:#若车在当前路是反向
                    start_per = 1.0 - start_per
    
                
                    
                if end_per * road_length <= start_per * road_length + path_length :
    
                    #卡口功能
                    if self.Roads[c.track[0][0]].is_monitor == True :#逆向行驶在该路且该路是卡口,需要能走出这条路,才能到该路的起点,才能算过卡口
                        self.monitor_record[self.Roads[c.track[0][0]].monitor_index].append( {'time':str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) ),'car_id':i} )
                    #卡口功能
                    
                    #车将开出当前路
                    #print '车将开出当前路'
                    #print 'path_length',path_length
                    #print 'start_per',start_per
                    #print 'end_per',end_per
                    path_length = start_per * road_length + path_length - \
                                  end_per * road_length
                    #print 'path_length',path_length
                    #print 'start_per',start_per
                    #print 'end_per',end_per
                    c.track = (c.track)[1:]
                    if len(c.track) > 0:#车还有新的路要走
                        c.road_id = c.track[0][0]#未来路id
                        c.road_percent = 0#已走未来路的百分比
                        c.dirc = c.track[0][2]#未来路走的方向
                    elif len(c.track) == 0:#车已经到终点
                        c.done = True
                        c.road_id = c.end[0]
                        c.road_percent = c.end[1]
                        c.dirc = c.end[2]
                        return
                else :#车走不完当前路
                    #print '车走不完当前路'
                    #c.road_id 不变
                        
                    c.road_percent = (start_per * road_length + path_length ) \
                                     / road_length
                    path_length = 0#还能走路长归0
                    c.dirc = -1
                    '''
                    print '车的当前路id%d路百分比%f方向%d'%(c.road_id,\
                                                c.road_percent,c.dirc)
                    '''

    def print_monitor_record(self):#打印所有卡口记录
        """
        function name: print_monitor_record,
            to store the corresponding records into the mongodb.
        """
        records = []
        for i in range(len(self.monitor_record)):
            if len(self.monitor_record[i]) == 0: 
                continue
            one_record = []
            for j in range(len(self.monitor_record[i])):
                print 'monitor_id: %d, time:%s, car_id:%d'%(self.monitor_id_list[i], \
                    self.monitor_record[i][j]['time'],int(self.monitor_record[i][j]['car_id']))
                one_record.append({
                    'car_id': int(self.monitor_record[i][j]['car_id']),
                    'time': self.monitor_record[i][j]['time'],
                })
            records.append({
                'monitor_id': int(self.monitor_id_list[i]),
                'record': one_record,
            })
        # store the info
        DBoperation.store_records(records)
        self.monitor_record = [[] for i in range(self.monitor_sum) ]
        return records

    def get_grids(self, level):
        """
        function name: get_grids,
            to get the target grids parameters, ie. the numbers of rows and the number
            of columns.
        input: level, an integer indicating the current level of the map.
        output: two integers. nrow & ncols.
        """
        return (15, 15)#栅格

#**************************************************************************************
#下面sub,add,mul函数都是辅助计算车的绝对坐标x与y的

def sub(i,j):#向量i-向量j
    return point(i.x - j.x , i.y - j.y)

def add(i,j):#向量 i与j相加
    return point(i.x + j.x , i.y + j.y)

def mul(i , p):#向量i与实数p相乘
    return point(i.x * p , i.y * p)

def Debug(flag,s): #flag为真,则打印列表s中的debug信息
    if flag:
        for i in range(len(s)):
            print s[i],
        print

#point中的id_p属性应该和它在Points列表中的编号一致
class point(object):
    def __init__(self , x , y , point_id = 0):
        self.x = x
        self.y = y
        self.id_p = point_id

#road中的id_r属性应该和它在Roads列表中的编号一致
class road(object):
    def __init__(self , road_id , start , end , length,is_monitor=False,monitor_id=-1):
        self.id_r = road_id             #路id
        self.start = start              #起点编号
        self.end = end                  #终点编号
        self.length = length            #路长
        self.is_monitor=is_monitor      #是否卡口标记位
        self.monitor_id=monitor_id      #卡口id
        self.monitor_index = -1         # used by RQ

class Car:
    """
    this defines a revised version of Car object.
    @date: 2014-07-14
    """
    def __init__(self, one_car_dict):
        """
        function name: __init__, 
            a initial function
        input: one_car_dict,
            a dict type argument for initializing the car.
        output: a Car object
        """
        self.car_id = int(one_car_dict['car_id'])
        self.car_color = one_car_dict['car_color']
        self.car_type = one_car_dict['car_type']
        self.y = float(one_car_dict['start_point_y'])
        self.x = float(one_car_dict['start_point_x'])
        self.track = [
            (int(one_passed_segment['segment_id']),
            1.0,
            int(one_passed_segment['direction'])) \
            for one_passed_segment in one_car_dict['tracks']['passed_segments']]

        self.v = float(one_car_dict['max_speed'])
        self.road_id = int(one_car_dict['tracks']['start_segment']['segment_id'])
        self.road_percent = float(one_car_dict['tracks']['start_segment']['percent'])
        self.dirc = int(one_car_dict['tracks']['start_segment']['direction'])
        self.end = (
            int(one_car_dict['tracks']['end_segment']['segment_id']),
            float(one_car_dict['tracks']['end_segment']['percent']),
            int(one_car_dict['tracks']['end_segment']['direction'])
        )
        self.start = (
            int(one_car_dict['tracks']['start_segment']['segment_id']),
            float(one_car_dict['tracks']['start_segment']['percent']),
            int(one_car_dict['tracks']['start_segment']['direction'])
        )
        self.done = False

    def __str__(self):
        """
        used when print the Car object
        """
        res = ''
        res += 'car_id: '       + str(self.car_id)       + '\n'
        res += 'x: '            + str(self.x)            + '\n'
        res += 'y: '            + str(self.y)            + '\n'
        res += 'track: '        + str(self.track)        + '\n'
        res += 'v: '            + str(self.v)            + '\n'
        res += 'road_id: '      + str(self.road_id)      + '\n'
        res += 'road_percent: ' + str(self.road_percent) + '\n'
        res += 'dirc: '         + str(self.dirc)         + '\n'
        res += 'end: '          + str(self.end)          + '\n'
        res += 'start: '        + str(self.start)        + '\n'
        res += 'done: '         + str(self.done)

        return res
