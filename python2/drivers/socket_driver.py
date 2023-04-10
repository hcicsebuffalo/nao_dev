import socket 
import pickle

class chatGPT(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.gui_socket = None

    
    def initSocket(self, PORT):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', PORT))
    
    def initGui(self, PORT):
        self.gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui_socket.connect(('127.0.0.1', PORT))
    
    def send_request(self):
        request = "chatGPT"
        self.client_socket.sendall(request.encode())
        print("request sent")

    def get_response(self):
        t  = self.client_socket.recv(1024)
        #print(t)
        try:
            result = pickle.loads(t)
            #print('Result:', result)
            return result
        except:
            print("Error in getting response")
            return None
        
    def socket_loop(self, nao, gui):
        while gui:
            t = self.gui_socket.recv(1024)
            try:
                result = pickle.loads(t)
                result = str(result)
                print('Gui Out ------- :', result)
                #return result
                if "dance" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/FunnyDancer_1")
                elif "take" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/TakePicture_1")
                elif "laugh" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Positive/Laugh_1")
                elif "sing" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/HappyBirthday_1")
            except:
                print("Error in getting response")
                #return None

            
 