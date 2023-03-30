import socket 
import pickle

class chatGPT(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
    
    def initSocket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 9993))
    
    def send_request(self):
        request = "chatGPT"
        self.client_socket.sendall(request.encode())
        print("request sent")

    def get_response(self):
        t  = self.client_socket.recv(1024)
        #print(t)
        result = pickle.loads(t)
        print('Result:', result)
        return result

 