import pika,sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# When RabbitMQ quits or crashes it will forget the queues and messages 
# unless you tell it not to. Two things are required to make sure that 
# messages aren't lost: we need to mark both the queue and messages as durable.
# channel.queue_declare(queue='hello', durable=True)
# RabbitMQ doesn't allow you to redefine an existing queue
# with different parameters and will return an error to any program that tries to do that
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
print(f" [x] Sent {message}")


connection.close()