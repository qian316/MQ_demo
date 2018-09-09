# _*_ coding:utf-8 _*_

# 发布/订阅 -- 日志消费端
# 把消费到的数据保存在log日志文件中。 python3 receive.logs > logs_from_rabbit.log

import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# 生成随机队列名
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# 断开连接后，队列会自动删除
result = channel.queue_declare(exclusive=True)

# 列表与交换机绑定
queue_name = result.method.queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(" [*] Waiting for logs. To exit press CTRL+C")

def callback(ch,method,properties,body):
    print(" [x] %r" %(body,))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()