import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# no need to declare a queue and bind it in this case
# only declare an exchange
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

# assume that 'severity' can be one of 'info', 'warning', 'error'
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(f"[x] Sent {severity}:{message}")

connection.close()