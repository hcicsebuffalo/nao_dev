import pika
import base64
import numpy as np


# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# Declare the image queue
channel.queue_declare(queue='image_queue')

# Define a callback function to process received messages
def callback(ch, method, properties, body):
    # Decode the image from base64 string
    image_bytes = base64.b64decode(body)
    
    # Process the image as needed
    # ...
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    print(len(image_np))

    # Acknowledge message receipt
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from the image queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='image_queue', on_message_callback=callback)

# Start consuming messages
channel.start_consuming()
