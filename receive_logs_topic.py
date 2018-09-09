# _*_ coding:utf-8 _*_
# 主题交换机demo，可以根据命令参数，接收不同消费端的消费数据
# 直接接收有关 test.* 的数据
# python3 receive_logs_topic.py test.*
# 组合多种规则 test.* *.demo，接收test.*和*.demo的所有生产数据
# python3 receive_logs_topic.py test.* *.demo

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# 根据传入的参数，队列来决定接收什么数据，让消费端消费
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

