import asyncio, psycopg2, json

from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    ConsumerOffsetSpecification,
    OffsetType
)

# add your postgres connection details here
POSTGRES_SERVER=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""
PSODGRES_PORT=5432

db_conn = psycopg2.connect(database=POSTGRES_DB,
                        host=POSTGRES_SERVER,
                        user=POSTGRES_USER,
                        password=POSTGRES_PASSWORD,
                        port=PSODGRES_PORT)

cursor = db_conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS customer_points (customer_id INT, points INT)")
db_conn.commit()
async def receive():
    STREAM_NAME = "customer_points_updates"
    # 5GB
    STREAM_RETENTION = 5000000000
    consumer = Consumer(host="localhost", username="guest", password="guest")
    # Note that the consumer part also declares the stream. This is to allow either part to be started first, be it the producer or the consumer.
    await consumer.create_stream(
        STREAM_NAME, exists_ok=True, arguments={"MaxLengthBytes": STREAM_RETENTION}
    )

    # we can add_signal_handler to the loop to gracefully shut down the app when the user clicks ctrl+c
    # did not add now to keep the app as simple as possible

    async def on_message(msg: AMQPMessage, message_context: MessageContext):
        stream = message_context.consumer.get_stream(message_context.subscriber_name)
        print("Got message: {} from stream {}".format(msg, stream))
        data = json.loads(msg)
        if data.get('transaction_type') == 'EARN':
            cursor.execute("SELECT * FROM customer_points WHERE customer_id = %s", (data.get('customer_id'),))
            customer_points_record = cursor.fetchone()
            print('current points balance:', customer_points_record[1])
            cursor.execute("UPDATE customer_points SET points = %s WHERE customer_id = %s", (int(customer_points_record[1]) + data['points'], data['customer_id']))
            cursor.execute("SELECT points FROM customer_points WHERE customer_id = %s", (data.get('customer_id'),))
            customer_points = cursor.fetchone()[0]
            print('new points balance:', customer_points)

    print("Press control +C to close")

    await consumer.start()
    await consumer.subscribe(
        stream=STREAM_NAME,
        callback=on_message,
        # read all messages in the stream starting from the very first message each time the consumer is started
        offset_specification=ConsumerOffsetSpecification(OffsetType.FIRST, None),
    )
    await consumer.run()
    await asyncio.sleep(1)

asyncio.run(receive())