import pika
import base64

# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# Load image file
with open('dog.jpeg', 'rb') as f:
    image_bytes = f.read()
    print(len(image_bytes))

# Encode image to base64 string
image_str = base64.b64encode(image_bytes).decode('utf-8')

# Publish image message to a queue
channel.queue_declare(queue='image_queue')
channel.basic_publish(exchange='', routing_key='image_queue', body=image_str)

# Close the connection
connection.close()
