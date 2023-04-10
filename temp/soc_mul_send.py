import socket
import pickle

HOST = '127.0.0.1'
PORT = 5094

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('Server is running...')

def handle_request(request):
    pass



while True:
    conn, addr = server_socket.accept()
    print('Connected by', addr)
    request = conn.recv(1024).decode()
    print('Request:', request)
    function = handle_request(request)
    if function:
        args = pickle.loads(conn.recv(1024))
        print('Arguments:', args)
        result = int(function(*args))
        print(result)
        conn.sendall(pickle.dumps([result] , protocol = 2))
    else:
        conn.sendall(b'Invalid request')
    conn.close()