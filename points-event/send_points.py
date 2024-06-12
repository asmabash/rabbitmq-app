import json, pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='points_queue')

customer_points_data = {"customer_id": 1, "program_id": 1,
                        "transaction_type":"EARN", "points": 10,
                        "purchase_amount": 50}

channel.basic_publish(exchange='',
                      routing_key='points_queue',
                      body=json.dumps(customer_points_data),
                      properties=pika.BasicProperties('points_added')) # name of event
print(f"Sent {customer_points_data}")

connection.close()