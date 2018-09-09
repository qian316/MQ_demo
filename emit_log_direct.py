# _*_ coding:utf-8 _*_

# 路由，日志记录，发送info、waring、error三种级别的日志
#发送info消息的格式  python3 emit_log_direct.py info "test"
#发送error消息的格式  python3 emit_log_direct.py error "test"


import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 直连交换机
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'

message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)

print(" [x] Sent {0}:{1}".format(severity,message))

connection.close()