import pika

# establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a hello queue to which the message will be delivered
# if we skip this, the message will be dropped
channel.queue_declare(queue='hello')

# In RabbitMQ a message can never be sent directly to the queue,
# it always needs to go through an exchange.
# The default exchange is an empty string
# The routing_key  parameter is name of queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()