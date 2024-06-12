import pika, sys, os

def main():
    # establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # no need to redeclare if we are sure send.py will be run first
    # however, if we don't know which file will run first, it is best practice to define it twice
    # it is idempotent
    # channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # this particular callback function should receive messages from our hello queue
    channel.basic_consume(queue='hello',
                        auto_ack=True,
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