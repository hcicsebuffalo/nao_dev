import socket
import pickle

HOST = '127.0.0.1'
PORT = 5006

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

request = input('Enter request (add/multiply): ')
print(request)
client_socket.sendall(request.encode())

if request == 'add' or request == 'multiply':
    args = []
    for i in range(2):
        args.append(int(input('Enter argument {}: '.format(i + 1))))
    client_socket.sendall(pickle.dumps(args))
    t  = client_socket.recv(1024)
    print(t)
    result = pickle.loads(t)
    print('Result:', result)
else:
    print(client_socket.recv(1024).decode())

client_socket.close()