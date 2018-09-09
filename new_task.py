# _*_ coding:utf-8 _*_
import pika
import sys

# 工作队列：消息确认 no_ack默认为false,消息持久话 durable =True

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode= 2,
                      ))
print(" [x] Sent %r" %(message,))
connection.close()