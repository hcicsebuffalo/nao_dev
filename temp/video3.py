import socket
import numpy as np
import pickle

# create a socket object
s = socket.socket()

# get local machine name
host = "127.0.0.1"

# set port number
port = 9335

# bind the socket to a specific port
s.bind((host, port))

# set the socket to listen for incoming connections
s.listen(1)

# wait for a client to connect
client_socket, addr = s.accept()

print("COnnection established")

# receive the serialized image
serialized_img = client_socket.recv(16777216)
print(len(serialized_img) , " -------------")

#deserialize the image using pickle
img = pickle.loads(serialized_img)

print(img)
#print the NumPy array



############

# received_data = b''
# while True:
#     # receive data in chunks
#     chunk = client_socket.recv(16777216)
#     #print("got")
#     if not chunk:
#         # all data has been received
#         break
#     received_data += chunk
#     if len (received_data) == 10:
#         pass

# print(" DOne ")

# # deserialize the image using pickle
# try:
#     img = pickle.loads(received_data)
#     print(len(img))
# except pickle.UnpicklingError as e:
#     # handle the error
#     print(f"Error: {e}")
#     img = None

# # print the NumPy array
# print(img)


############



# close the client socket connection
client_socket.close()

# close the server socket connection
s.close()
