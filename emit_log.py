# _*_ coding:utf-8 _*_

# 发布/订阅 -- 日志生产端
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

channel = connection.channel()

# 创建logs交换机，类型为扇型
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "inof：Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='', # 路由密匙为空
                      body=message)

print(" [x] Sent %r" %(message,))
connection.close()