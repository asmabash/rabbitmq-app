import asyncio, json
from rstream import Producer

customer_points_data = {"customer_id": 1, "transaction_type":"EARN", "points": 10}
async def send():
    async with Producer(
            host="localhost",
            username="guest",
            password="guest",
        ) as producer:
        
        STREAM_NAME = "customer_points_updates"
        STREAM_RETENTION = 5000000000 # 5GB

        await producer.create_stream(
                    STREAM_NAME, exists_ok=True, arguments={"MaxLengthBytes": STREAM_RETENTION}) # stream is limited to be 5 GB in size

        await producer.send(stream=STREAM_NAME, message=json.dumps(customer_points_data).encode('utf-8'))
        print(f" [x] MESSAGE {json.dumps(customer_points_data)} sent")
        await producer.close()

        input(" [x] Press Enter to close the producer  ...")

asyncio.run(send())
