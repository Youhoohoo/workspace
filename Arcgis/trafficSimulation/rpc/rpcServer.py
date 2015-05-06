#!/usr/bin/env python
import pika
import os
import traceback
import sys
import callTable
import controller
import re
import json

# import config
file_path = os.path.realpath(__file__)
file_dir_path = os.path.split(file_path)[0]
sys.path.insert(0, os.path.join(file_dir_path, '..') )
import config
sys.path.remove( sys.path[0] )

# main controller, ie. the center of the simulation
controller = controller.Controller()

class SimulationRpcServer(object):
    """
    This server stays with the simulator. The simulator plays as the rpc server
    at this moment, serving the real-time data to the rpc client.
    """
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=config.RPC_HOST))
        
        self.channel = connection.channel()
        
        self.channel.queue_declare(queue=config.RPC_ROUTING_KEY)

    def start(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, config.RPC_ROUTING_KEY)
        
        print " [x] Awaiting RPC requests"
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        print ' [X] Receiving request '
        try:
            response = self.transfer(body)
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                             body=str(response))
            ch.basic_ack(delivery_tag = method.delivery_tag)
            print ' [X] response:'
        except:
            traceback.print_exc()

    def transfer(self, body):
        """
        function name: transfer,
            To transfer the request. To call different processes of the 
            simulator according to the message body.
        input: body, the message body
        output: corresponding response
        """
        try: 
            # body = str(body)
            body = json.loads(body)
            for k,v in callTable.call_table.items():
                if k == str(body['method']):
                    cmd = 'controller.' + str(v) + '("""' + str(body['arg']) + '""")'
                    cmd_original = ('controller.' + str(v) + \
                        '("""' + json.dumps(body['arg']) + '""")')
                    result = eval(cmd_original)
                    return json.dumps( {'result': result} )
        except:
            traceback.print_exc()
            return ''


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def __main__():
    simulation_rpc_server = SimulationRpcServer()
    simulation_rpc_server.start()

if __name__ == '__main__':
    __main__()
