import pika
import os
import time
import json

host = os.getenv("RABBITMQ_HOST", "rabbitmq")
my_queue = os.getenv("MY_QUEUE")
next_queue = os.getenv("NEXT_QUEUE")

while True:
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        break
    except pika.exceptions.AMQPConnectionError:
        time.sleep(2)

ch = conn.channel()
ch.queue_declare(queue=my_queue, durable=True)
if next_queue:
    ch.queue_declare(queue=next_queue, durable=True)


def on_message(ch, method, properties, body):
    try:
        msg = json.loads(body.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    print(f"Got {msg}", flush=True)

    if next_queue:
        ch.basic_publish(exchange="", routing_key=next_queue, body=json.dumps(msg))
        print(f"Send {msg}", flush=True)
    else:
        print(f"Success. Message ", flush=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue=my_queue, on_message_callback=on_message)
ch.start_consuming()
