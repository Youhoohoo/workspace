#!/usr/bin/python2.7
#coding=utf-8

import json
import web
import messagechannel
import os
import sys
import config

filePath = os.path.realpath(__file__)
fileDirPath = os.path.split(filePath)[0]

# import rpcClient
sys.path.insert(0, os.path.join(fileDirPath,'rpc') )
import rpcClient
sys.path.remove(sys.path[0])

# import the db 
sys.path.insert(0, os.path.join(fileDirPath,'db') )
import DBoperation
sys.path.remove(sys.path[0])


import globalvars
import web
import pika
import time
import traceback

render = web.template.render('./templates')

# some global vars

# SIMULATION_PLAYING_STATE: 
# 0: as the initial value
# -1: palying stopped
# 1: start palying, or continue playing
# 2: pause playing
SIMULATION_PLAYING_STATE = 0

urls = (
    '/', 'Index',
    '/test', 'Test',
    '/getConf', 'GetConf',
    '/selectConf', 'SelectConf',
    '/([1,2,3,4])', 'Messagereq',
    '/changeState', 'ChangeState',
    '/heartBeatResponse', 'HeartBeatResponse',
    '/helloworld', 'HelloWorld',
    '/login', 'Login',
    '/admin', 'Admin',
    '/fetchrecords', 'FetchRecords',
    '/fetchsolutioninfo', 'FetchSolutionInfo',
)
app = web.application(urls, globals())
web.config.debug = False

# get rpc client, thus be able to send requests to simulator
simulation_rpc_client = rpcClient.SimulationRpcClient() 

if web.config.get("_session") is None:
    from web import utils
    store = web.session.DiskStore('sessions')
    user = utils.Storage({
                          "id": "",
                          "name": "",
                          "password": "",
                          })
    session = web.session.Session(app, store, 
                                  initializer={
                                               "status": 0,
                                               "user": user,
                                               })
    web.config._session = session
else:
    session = web.config._session

class Index:
    def GET(self):
        if not session.status:
            return render.login()
        user_data = web.input()
        return render.index()
    def POST(self):
        user_data = web.input()
        #print user_data.name, user_data.age
        return 'hello boy from post'

class Test:
    def GET(self):
        # here to send back raw points.
        # return render.test()
        ret = simulation_rpc_client.send_request({'method': 'test_fetch_points',
                                                  'arg': '10'})
        return json.dumps(ret)

    def POST(self):
        return 'test of post'


class GetConf:
    def GET(self):
        return ''
    def POST(self):
        conf = []
        carConf = []
        carConf = DBoperation.fetch_init_cars_general()
        conf.append(carConf)
        trafficLightConf = []
        trafficLightConf.append({'light_solution_id': 1,
                                 'light_solution_name': 'trafficLightConf_1',
                                 'description': 'traffic light'})
        conf.append(trafficLightConf)
        return json.dumps(conf)

class SelectConf:
    def GET(self):
        pass
    def POST(self):
        # when the user confirms a solution, then tell the simulation
        # component to initialize with this set of solution. 
        # Actually the rpcServer controls the simulation, thus just pass
        # over the commands to the rpcServer.
        try:
            user_para = web.input()
            solution_id = user_para.solution_id
            res = simulation_rpc_client.send_request({
                'method': 'select_conf',
                'arg': {'car_solution_id': solution_id}
            })
            return json.dumps(res)
        except:
            traceback.print_exc()
            return False


class Messagereq:
    def GET(self,path):
        message = messagechannel.produceMessagereq("message req",path)
        return "Hello, req , " + message + "  " + time.ctime()


class ChangeState:
    def POST(self):
        params= web.input()
        global SIMULATION_PLAYING_STATE
        SIMULATION_PLAYING_STATE = params.state
        return json.dumps({'STATE': SIMULATION_PLAYING_STATE})


class HeartBeatResponse:
    def POST(self):
        params = web.input()
        xmin = params.xmin
        xmax = params.xmax
        ymin = params.ymin
        ymax = params.ymax
        level = params.level

        res = simulation_rpc_client.send_request({
            'method': 'update_simulation',
            'arg': {
                'lefttop_x': xmin,
                'lefttop_y': ymax,
                'rightbottom_x': xmax,
                'rightbottom_y': ymin,
                'level': level,
                'target_time': 1,
            }
        })
        res = {'points': res}
        return json.dumps(res)


class HelloWorld:
    def GET(self):
        return render.HelloWorld()


class Login:
    def GET(self):
        return render.login()
    def POST(self):
        #接收前台页面输入的值，在判断登录
        user_data = web.input()
        username = str(user_data.un)
        password = str(user_data.pwd)
        userid = DBoperation.verify(username, password)
        if userid  != -1:#修改链接数据库判断
            session['user']['name'] = username
            session['user']['password'] = password
            session['user']['id'] = userid
            session['status'] = 1

            return json.dumps({'message': '登录成功！', 'id': 1})
        else:
            return json.dumps({'message': '帐号或密码有误!', 'id': -1})


class Admin:
    def GET(self):
        user_data = web.input()
        return render.adminManage()
    def POST(self):
        dbhelper = DBHelper.DBHelper('192.168.14.188')
        db = dbhelper.db
        user_data = web.input()
        temp_user = dict(userID=user_data['manNo'], password=user_data['manPw'], username=user_data['manName'])
        db.user.insert(temp_user)

        print user_data
        ##print user_data.name, user_data.age 
        return 'hello boy from post'

class FetchRecords:
    """
    fetch monitors, ie, the cameras
    """
    def POST(self):
        try:
            monitor_id = int(web.input().monitor_id)
            # print '*'*10, monitor_id
            return json.dumps(DBoperation.fetch_records(monitor_id))
        except:
            traceback.print_exc()
            return json.dumps([])

class FetchSolutionInfo:
    def GET(self):
        solution_id = int(web.input().solution_id)
        return json.dumps(DBoperation.fetch_solution_info(solution_id))
    def POST(self):
        try:
            solution_id = int(web.input().solution_id)
            return json.dumps(DBoperation.fetch_solution_info(solution_id))
        except:
            traceback.print_exc()
            return json.dumps([])

if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        traceback.print_exc(e)
    finally:
        pass
