import pika, sys, os, time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # In order to make sure a message is never lost, 
    # RabbitMQ supports message acknowledgments. 
    # An ack(nowledgement) is sent back by the consumer to 
    # tell RabbitMQ that a particular message had been received, 
    # processed and that RabbitMQ is free to delete it.

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        # simulate a long task, for every dot in the message, sleep for 1 second
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)


    channel.basic_consume(queue='hello',
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)