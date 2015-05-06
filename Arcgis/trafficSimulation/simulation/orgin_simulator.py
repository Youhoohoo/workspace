#!/usr/bin/python2.7
#coding=utf-8

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
        

class car(object):
    def __init__(self , car_id , dirc , road_id , road_percent ,\
                 end = () , x = -1.0 , y = -1.0 , track = [] , v = 50.0 , done = False):
        self.car_id = car_id            #车id
        self.x = x                      #车坐标X
        self.y = y                      #车坐标Y
        self.track = track              #车轨迹，是一个按序包含了车路径所有的
        #（路id，需要走的路百分比，正向or反向）三元组的列表
        self.v = v                      #车速度
        self.road_id = road_id          #车当前所在路的id
        self.road_percent = road_percent#车在当前路已经走百分之多少
        self.dirc = dirc                  #车在该路是正向(+1)计算的还是逆向(-1)计算的
        self.end = end                  #终点（路id,需要走的路百分比，正向or反向）
        #end是一个与start相同格式的三元组
        self.start = start
        self.done = done                #车是否已经到达终点

def Debug(flag,s):  
    #flag为真,则打印列表s中的debug信息
    if flag:
        for i in range(len(s)):
            print s[i],
        print

#***************************1.2生成随机的车************************************
#下面sub,add,mul函数都是辅助计算车的绝对坐标x与y的

def sub(i,j):#向量i-向量j
    return point(i.x - j.x , i.y - j.y)

def add(i,j):#向量 i与j相加
    return point(i.x + j.x , i.y + j.y)

def mul(i , p):#向量i与实数p相乘
    return point(i.x * p , i.y * p)

def get_random_car():   #生成car_num辆随机车
    car_id = -1
    for i in range(car_num):
        car_id += 1
        road_id = random.randint(0 , len(Roads) - 1)
        road_percent = random.random()
        dirc = random.choice([-1 , 1])
        end_road_id = random.randint(0 , len(Roads) - 1)
        end_road_percent = random.random()
        end_dirc = random.choice([-1 , 1])
        end = (end_road_id , end_road_percent , end_dirc)
        
        #下面几行是计算车的初始坐标x与y的代码
        per = road_percent
        if dirc == -1:
            per = 1.0 - per
        s = Roads[road_id].start    #车起点所在路的 start点编号
        e = Roads[road_id].end      #车起点所在路的 end点编号
        p = add(Points[s] , mul(sub(Points[e] , Points[s]) , per))#向量运算
        x = p.x   #车x坐标
        y = p.y   #车y坐标
        
        car_r = car(car_id = car_id , dirc = dirc , road_id = road_id ,\
                    road_percent = road_percent , end = end , x = x , y = y)
        Cars.extend([car_r])

    flag = 0
    Debug(flag , ['车的总数为:' , len(Cars)])
    for i in range(len(Cars)):
        c = Cars[i]
        Debug(flag , ['车id'      ,   c.car_id        ,   ' ',
                      '方向'      ,    c.dirc          ,   ' ',
                      '路id'      ,    c.road_id       ,   ' ',
                      '路百分比'   ,    c.road_percent  ,   ' ',
                      '终点'      ,    c.end           ,   ' ',
                      'x坐标'     ,    c.x             ,   ' ',
                      'y坐标'     ,    c.y             ,   ' ',
                      'track'    ,    c.track         ,   ' ',
                      '速度'      ,    c.v             ,   ' ',
                      'done'     ,    c.done          ,   ' '
                      ])
        
def get_decided_car():
#仅用于测试,获得一确定的车信息
    car_id = 0
    road_id = 5
    road_percent = 0.21
    dirc = -1
    end_road_id = 50000
    end_road_percent = 0.38
    end_dirc = 1
    end = (end_road_id , end_road_percent , end_dirc)

#下面几行是计算车的初始坐标x与y的代码
    per = road_percent
    if dirc == -1:
        per = 1.0 - per
    s = Roads[road_id].start    #车起点所在路的 start点编号
    e = Roads[road_id].end      #车起点所在路的 end点编号
    p = add(Points[s] , mul(sub(Points[e] , Points[s]) , per))#向量运算
    x = p.x   #车x坐标
    y = p.y   #车y坐标
        
    car_r = car(car_id = car_id , dirc = dirc , road_id = road_id ,\
                road_percent = road_percent , end = end , x = x , y = y)
    Cars.extend([car_r])


#***************************1.3生成车的轨迹************************************

def get_positive_length(start):
    '''
    给出一个start =（road_id，percent，dirc）三元组，返回车当前在路的正方向上已经走了多长距离.
    '''
    if start[2] == 1 :
        return Roads[start[0]].length * start[1]
    else :
        return Roads[start[0]].length * (1.0-start[1])
    
def get_path_value(i,j):    #返回i节点到j节点的最短距离
    filename = 'D:\\path\\' + '%d.txt'%(i)
    file = open(filename)
    for k in range(j + 1):    #注意这里是j+1,而不是j
        line = file.readline()
    file.close()
    return (float)((line.split(' '))[0])

def get_path_point(i , j):    #返回i节点到j节点的最短路中j前一个点编号
    filename = 'D:\\path\\' + '%d.txt'%(i)
    file = open(filename)
    for k in range(j + 1):
        line = file.readline()
    file.close()
    return (int)((line.split(' '))[1])

def get_path_track(i , j) :    #返回从i到j最短路径的点轨迹列表
    beg = i
    end = j
    res = [i];
    while beg != end :
        res.insert(1 , end)
        end = get_path_point(beg , end)
    return res

#计算出所有Cars的最短路径轨迹
def get_car_track(): 
#首先生成车的路径track
    num = 0
    for i in Cars:
        track = []
        num = num + 1
        if i.start[0] == i.end[0] :#车的起点与终点在同一条路上
            if get_positive_length(i.start) < get_positive_length(i.end):
            #起点与终点在同一条路上，且从路的正向看来，车的起点离路的起点更近
                track.extend([((i.start)[0] , 1 , 1)])
            else :
            #起点与终点在同一条路上，且从路的正向看来，车的起点离路的起点更远
                track.extend([((i.start)[0] , 1 , -1)])
            print '%d 当前车起点到终点的最小距离为'%(num) , min_length
            
        else :#车的起点与终点不在同一条路中
            p1=Roads[i.start[0] ].start    #车起点所在路的 起点
            p2=Roads[i.start[0] ].end      #车起点所在路的 终点
            p3=Roads[i.end[0] ].start      #车终点所在路的 起点
            p4=Roads[i.end[0] ].end        #车终点所在路的 终点
            
            length_start_positive = get_positive_length(i.start)
            #车起点 离它起点所在路 起点的距离
            
            length_start_negative = Roads[(i.start)[0]].length - \
                                    get_positive_length(i.start)
            #车起点 离它起点所在路 终点的距离            
            
            length_end_positive = get_positive_length(i.end)           
            #车终点 离它终点所在路 起点的距离            
         
            length_end_negative = Roads[ (i.end)[0] ].length - \
                                  get_positive_length(i.end)
            #车终点 离它终点所在路 终点的距离
            '''
            print 'length_start_positive',length_start_positive
            print 'length_start_negative',length_start_negative
            print 'length_end_positive',length_end_positive
            print 'length_end_negative',length_end_negative
            '''
            
            '''
            共4总组合需要判断：
            1.（车起点所在路的起点 p1，车终点所在路的起点p3）
            2.（车起点所在路的起点 p1，车终点所在路的终点p4）
            3.（车起点所在路的终点 p2，车终点所在路的起点p3）
            4.（车起点所在路的终点 p2，车终点所在路的终点p4）
            '''
            length_1 = get_path_value(p1 , p3)#得到p1到p3点的最短距离
            length_2 = get_path_value(p1 , p4)
            length_3 = get_path_value(p2 , p3)
            length_4 = get_path_value(p2 , p4)

            '''
            print 'path_value[%d][%d] is :'%(p1,p3),path_value[p1][p3]
            print 'path_value[%d][%d] is :'%(p1,p4),path_value[p1][p4]
            print 'path_value[%d][%d] is :'%(p2,p3),path_value[p2][p3]
            print 'path_value[%d][%d] is :'%(p2,p4),path_value[p2][p4]
            '''
            
            #各种情况再加上串联的首尾两段
            length_1 += length_start_positive + length_end_positive
            length_2 += length_start_positive + length_end_negative
            length_3 += length_start_negative + length_end_positive
            length_4 += length_start_negative + length_end_negative

            #求出最短路径
            start = p1
            end = p3
            dirc_start = -1 #表示车在起点所在路 所走的方向 正向1 负向-1
            dirc_end = 1    #表示车在终点所在路 所走的方向 正向1 负向-1
            min_length = length_1
            for j in [length_2 , length_3 , length_4]:
                if min_length > j:
                    min_length = j
            if min_length == length_1:
                start = p1
                end = p3
                dirc_start = -1
                dirc_end = 1  #注意这里是1,不是-1,车走到终点所在路的时候是从 那条路的起点进去然后到终点的,所以是正向
            elif min_length == length_2:
                start = p1
                end = p4
                dirc_start = -1
                dirc_end = -1
            elif min_length == length_3:
                start = p2
                end = p3
                dirc_start = 1
                dirc_end = 1
            elif min_length == length_4:
                start = p2
                end = p4
                dirc_start = 1
                dirc_end = -1

            '''
            print 'length_1',length_1
            print 'length_2',length_2
            print 'length_3',length_3
            print 'length_4',length_4
            '''
            
            print '%d 当前车起点到终点的最小距离为'%(num),min_length
            
            if min_length >= 1000000000.000000 :
                i.track = []
                i.done = True
                continue
            track.extend( [ ( (i.start)[0] , 1 , dirc_start ) ] )
            path = get_path_track(start , end)
            for j in range( len( path ) - 1):
                j1 = path[j]    #最短路径中一段的起点编号
                j2 = path[j + 1]  #最短路径中一段的终点编号
                if dict_road.has_key( (j1 , j2) ):#正向走该路
                    track.extend( [(dict_road[(j1 , j2)] , 1.0 , 1 )])
                elif dict_road.has_key( (j2 , j1) ):  #反向走该路
                    track.extend( [(dict_road[(j2 , j1)] , 1.0 , -1 )])
            track.extend( [ ( (i.end)[0] , 1 , dirc_end ) ] )
        i.track = track #将轨迹赋值给车

        file_handle =  open ( car_info_file , 'a' )
        if i.done == True :
            continue
        file_handle.write ( str(i.car_id)       + '\n' )
        file_handle.write ( str(i.dirc)         + '\n' )
        file_handle.write ( str(i.road_id)      + '\n' )
        file_handle.write ( str(i.road_percent) + '\n' )
        file_handle.write ( str(i.end[0])       + ' ' +\
                            str(i.end[1])       + ' ' +\
                            str(i.end[2])       + '\n')
        file_handle.write ( str(i.x)            + '\n' )
        file_handle.write ( str(i.y)            + '\n' )
        file_handle.write ( str(i.v)            + '\n' )
        file_handle.write ( str(i.done)         + '\n' )
        for ct in i.track:
            file_handle.write ( str(ct[0]) + ' ' + str(ct[1]) + ' ' + str(ct[2]) + '\n' )
        file_handle.write ( '#########################################################\n' ) #标记轨迹已经结束

        file_handle.close() #关闭文件

        flag = 0
        if flag :
            for r in path:
                print r
            print "min_len:" , min_length
            for r in i.track:
                print r[0] , ' ' , r[2]


def save_car_info():    #将所有车辆的信息都保存在txt文件中
    file_handle =  open ( car_info_file , 'a' )
    print 'fff'
    for c in Cars:
        print 'rrr'
        if c.done == True :
            continue
        print 'ccc'
        file_handle.write ( str(c.car_id)       +   '\n' )
        file_handle.write ( str(c.dirc)         +   '\n' )
        file_handle.write ( str(c.road_id)      +   '\n' )
        file_handle.write ( str(c.road_percent) +   '\n' )
        file_handle.write ( str(c.end[0])       +   ' ' +\
                            str(c.end[1])       +   ' ' +\
                            str(c.end[2])       +   '\n')
        file_handle.write ( str(c.x)            +   '\n' )
        file_handle.write ( str(c.y)            +   '\n' )
        file_handle.write ( str(c.v)            +   '\n' )
        file_handle.write ( str(c.done)         +   '\n' )
        for i in c.track:
            file_handle.write ( str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n' )
        file_handle.write ( '#########################################################\n' ) #标记轨迹已经结束

    file_handle.close() #关闭文件

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
    car_info_file = 'car_info.txt'         #保存一个车辆对象的所有信息的文件
    monitor_sum = 0
    monitor_record = []
    monitor_id_list = []        # store all the monitors' id in this list
    
    #***************************全局数据************************************

    #***************************1.1读图************************************
    #读point与road的所有信息
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
            new_point = point(x,y,point_id)
            self.Points.extend([new_point])
    
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
    
    def read_monitor(self, l):  #读卡口的所有信息
        # l = fetch_monitor_info()
        self.monitor_sum = len(l)
        self.monitor_record  = [[] for i in range(self.monitor_sum) ]
        for i in range(len(l)):
            monitor_index = i # int(l[i]['monitor_id'])
            monitor_id = int(l[i]['monitor_id'])
            segment_id = int(l[i]['segment_id'])
    
            self.Roads[segment_id].is_monitor = True
            self.Roads[segment_id].monitor_id = monitor_id
            self.monitor_id_list.append( monitor_id )
            self.Roads[segment_id].monitor_index = monitor_index


    #***************************2.1模拟车辆前进************************************
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
            
    def read_car_db(self, car_dict):
        self.Cars = []
        for one_car_dict in car_dict:
            car_obj = Car(one_car_dict)
            self.Cars.append(car_obj)

    def read_car_info(self):
        self.Cars = []
        self.car_num = 0 #记录读入了多少量车
        #all_done = False    #已经读取完毕?
        f =  open ( self.car_info_file , 'r' )
        while f.readline() :
            car_id = self.car_num + 1;
            dirc = int(f.readline())
            road_id = int(f.readline())
            road_percent = float(f.readline())
            
            rs = (f.readline()).split(' ')
            end = (int(rs[0]) , float(rs[1]) , int(rs[2]) )
    
            x = float(f.readline())
            y = float(f.readline())
            v = float(f.readline())
    
            rs = f.readline()
            done = True
            if rs[0] == 'F':
                done = False
            track = []
            
            while True:
                rs = (f.readline())
                
                if rs[0] == '#' :
                    #print rs
                    #xxx = raw_input()
                    break
                else:
                    rs = rs.split(' ')
                    #print rs
                    track.extend([(int(rs[0]) , float(rs[1]) , int(rs[2]))])
    
            car_r = car(car_id = car_id , dirc = dirc , road_id = road_id ,\
                        road_percent = road_percent , end = end , x = x ,\
                        y = y , track = track , v = v , done = done)
            self.Cars.extend([car_r])
    
            self.car_num = self.car_num + 1
        
    
    def test_print_car_info(self):
        print 'Cars len is %d'%(len(self.Cars))
        for c in self.Cars:
            print c.car_id
            print c.dirc
            print c.road_id
            print c.road_percent
            print c.end
            print c.x
            print c.y
            print c.track
            print c.v
            print c.done
            print '##############'

    def update(self, target_time):
        """
        notes
        """
        try:
            target_time = float(target_time)
            res = []
            for i in range(len(self.Cars)):
                self.get_new_car(target_time , i)
               # print ('[%f,%f]')%((get_pos(i))[0],(get_pos(i))[1] )
                res.append({
                    'x': self.get_pos(i)[0],
                    'y': self.get_pos(i)[1],
                    'density': 1
                })
            return res
        except:
            traceback.print_exc()
            return []

    def get_grids(self, level):
        """
        function name: get_grids,
            to get the target grids parameters, ie. the numbers of rows and the number
            of columns.
        input: level, an integer indicating the current level of the map.
        output: two integers. nrow & ncols.
        """
        return (15, 15)

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
                
        self.print_monitor_record()
        
        return final_res


    
#***************************1 初始化******************************************
def init():
    read_map()  #读point与road的所有信息

    read_monitor()  #读卡口的所有信息

    #get_random_car()    #生成car_num辆随机车 #get_decided_car()   #生成确定的一辆车

    #get_car_track() #计算出所有Cars的最短路径轨迹

    #save_car_info()
    
    #read_car_info()
    import sys
    sys.path.insert(0, '../db')
    import DBoperation
    sys.path.remove( sys.path[0] )
    read_car_db(DBoperation.fetch_init_cars_detail(1))

    
    #test_print_car_info()

if __name__ == '__main__':
    init()  #初始化点,路,车的信息与轨迹

