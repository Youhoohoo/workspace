#!/usr/bin/env python
import pika
import uuid
import os
import sys
import json

# import config
file_path = os.path.realpath(__file__)
file_dir_path = os.path.split(file_path)[0]
sys.path.insert(0, os.path.join(file_dir_path, '..') )
import config
sys.path.remove( sys.path[0] )

class SimulationRpcClient(object):
    """
    this client class will stays together with webServer. Thus the webServer can 
    yield a remote-process-call process, to get the corresponding data from the 
    simulator.
    """
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=config.RPC_HOST))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def send_request(self, content):
        """
        function name: send_request,
            to send the dict type data to the rpc server, ie. the traffic simulator.
        input: content, a dict type data
        output: the response from the simulator. Also the dict type data.
        """
        content = json.dumps(content)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=config.RPC_ROUTING_KEY,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(content))
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)['result']

def __main__():
    simulation_rpc_client = SimulationRpcClient()
    
    print " [x] Requesting "
    response = simulation_rpc_client.send_request(
        {'method': 'test_method', 
         'arg': {'key': 'test 30 way'}}
    )
    print " [.] Got %r" % (response,)
    
    print " [.] Got ", simulation_rpc_client.send_request(
        {'method': 'test_fetch_points', 
         'arg': {'num':'10'}}
    )


if __name__ == '__main__':
    __main__()
