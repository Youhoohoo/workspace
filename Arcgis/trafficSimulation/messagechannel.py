#!/usr/bin/env python
#coding=utf8
import pika
import simplejson as json
import threading
import time

ack = 0;

class MessageChannel:
    def __init__(self,msgreq_key,severity):
        self.msg = '';
        self.msgqueue = msgreq_key
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.cl = self.conn.channel()
        self.cl.queue_declare(queue=self.msgqueue)
        self.getinfo = False
        self.severity = severity
        sc = messageproduceThread(self)
        sc.start()

    def callback(self,ch, method, properties, body):
        self.msg = body
        self.getinfo = True
        #ch.basic_ack(delivery_tag = method.delivery_tag)
        print 'hehe' + str(body)
        method_frame, header_frame, body = ch.basic_get(queue = self.msgqueue) 
        #self.cl.basic_get(queue = self.msgqueue) 
        #print 'method_frame.NAME: ' + method_frame.NAME
        if method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
        #else:
        #    print "[x] Received %r" % (self.msg,) + time.ctime()
        #    ch.basic_ack(delivery_tag = method.delivery_tag)
    def start_consuming(self):
        self.cl.basic_consume(self.callback,queue=self.msgqueue)
        self.cl.start_consuming()
    def stop_consuming(self):
        self.cl.stop_consuming()
        self.cl.close()
        self.conn.close()

    def produce(self,message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='direct_req',
                         type='direct')
        global ack
        message += '@' + str(ack)
        channel.basic_publish(exchange='direct_req',
                      routing_key=self.severity,
                      body=message)
        ack += 1;
        print "[x] Sent %r:%r" % (self.severity, message) + time.ctime()
        channel.close()
        connection.close()
        self.getinfo = False
        i = 0
        while((self.msg =='' or self.getinfo == False) and i<100): 
            i += 1
            time.sleep(0.05)
        temp = self.msg
        if(self.msg=='' or self.getinfo == False): 
            temp = 'time out'
            conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            chn = conn.channel()
            chn.basic_publish(exchange='',
                      routing_key=self.msgqueue,
                      body=temp)
            chn.close()
            conn.close()
        self.msg==''
        return temp

class messageproduceThread(threading.Thread):
    def __init__(self,messagechanel):
        threading.Thread.__init__(self)
        self.messageChanel = messagechanel
    def run(self):
        self.messageChanel.start_consuming()

def produceMessagereq(message,severity):
    global ack
    messagereq = MessageChannel(str(ack),severity)
    message = messagereq.produce(message)
    try:
        messagereq.stop_consuming()
    except:
        pass
    del messagereq
    return message
