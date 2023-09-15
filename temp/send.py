import pika
import base64
import time 


# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# Receive string message from PC2
def callback(ch, method, properties, body):
    print("Received message: %r" % body)


# Load image file
with open('dog.jpeg', 'rb') as f:
    image_bytes = f.read()
    print(len(image_bytes))

# Encode image to base64 string
image_str = base64.b64encode(image_bytes).decode('utf-8')


print(" cp 1")
# Publish image message to a queue
channel.queue_declare(queue='image_queue')
channel.queue_declare(queue='string_queue')

print(" cp 2")

channel.basic_consume(queue='string_queue', on_message_callback=callback, auto_ack=True)

print(" cp 3")

i = 0

while i < 100:
    channel.basic_publish(exchange='', routing_key='image_queue', body=image_str)
    i += 1
    channel.start_consuming()
    print(" Sent ")
    time.sleep(2)

connection.close()


# # Close the connection to PC2
# connection.close()