import socket 
import pickle
import threading

class chatGPT(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.gui_socket = None

        self.dance_sckt = None
        self.play_song_sckt = None

    def load_function(self, nao, dance, play_song):
        #self.dance = dance
        #self.play_song = play_song

        self.dance_sckt = threading.Thread( target= nao.dance )
        self.play_song_sckt = threading.Thread( target= nao.play_song)

    
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
            #if result[0:4] == "gpt":
            print("Response sent")
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
                #print("Error in getting response")
                pass
                #return None
    def process_res_(self, res):
        out = ''
        res = res[2:-2]
        for elem in res:
            if elem.isalnum() or elem == ' ' or elem == ".":
                out += elem 
        return out
    
    
    def wake_wrd_loop(self, nao, wake):
        while wake and not nao.gpt_request:
            t  = self.client_socket.recv(1024)
            try:
                result = self.process_res_( str(pickle.loads(t)) )
                print('Result: -- ', result)
                #print("Wake word Response : \n " , result)
                if result == "Dance":
                    print("I am Dancing")
                    self.dance_sckt.start()
                    self.play_song_sckt.start()
                    ## Changes added for continous dance
                    #     if not self.dance.is_alive():
                    #         self.dance = threading.Thread( target= self.nao.dance )
                    #         self.dance.start()
                    while self.play_song_sckt.is_alive():
                        #if not self.dance.is_alive():
                        #    self.dance = 
                        pass
                    
                    self.dance_sckt = threading.Thread( target= nao.dance )
                    self.play_song_sckt = threading.Thread( target= nao.play_song )

                else:
                    print("....")
                    try:
                        nao.sayText( str(result) )
                        
                    except:
                        nao.sayText( "Sorry I am not able to process your request for a moment" )
                        #nao_.sayText("Sorry I am not able to process your request for a moment")
                    print(" Said")


            except:
                #print("Error in getting response")
                #return None
                pass
 