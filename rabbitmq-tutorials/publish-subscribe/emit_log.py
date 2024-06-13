import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

result = channel.queue_declare(queue='', # let the server choose a random queue name
                               exclusive=True) # once the consumer connection is closed, the queue should be deleted

# fanout broadcasts all the messages it receives to all the queues binded to it
# ideal for the broadcast routing of messages
# Ex. distributed systems can broadcast state and configuration updates
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
channel.queue_bind(exchange='logs',
                   queue=result.method.queue)

message = ' '.join(sys.argv[1:]) or "info: Hello World!"


# we need to supply a routing_key when sending, but its value is ignored for fanout exchanges
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(f"Sent {message}")

connection.close()