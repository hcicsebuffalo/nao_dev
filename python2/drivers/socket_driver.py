import socket 
import pickle
import threading
import ast

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

        self.dance_sckt = threading.Thread( target= nao.dance_nao )
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
                elif "scratchhead" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/ScratchHead_1")
                elif "zombie" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/Zombie_1")
                elif "hungry" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Positive/Hungry_1")
                elif "embarassed" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Neutral/Embarrassed_1")
                elif "attention" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Neutral/AskForAttention_1")
                elif "fear" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Negative/Fear_1")
                elif "hurt" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Negative/Hurt_1")
                elif "relieved" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Positive/Relieved_1")
                elif "hideeyes" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/HideEyes_1")
                elif "kungfu" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/KungFu_1")
                elif "loveyou" in result.lower():
                    nao.behave.startBehavior("nimations/Stand/Waiting/LoveYou_1")
                elif "relaxed" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/Relaxation_2")
                elif "scratchbottom" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/ScratchBottom_1")
                elif "space" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/SpaceShuttle_1")
                elif "taxi" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/Taxi_1")
                elif "mischievous" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Neutral/Mischievous_1")
                elif "sneeze" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Neutral/Sneeze")
                elif "surprise" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Negative/Surprise_1")
                elif "suspicious" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Neutral/Suspicious_1")
                elif "ecstatic" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Positive/Ecstatic_1")
                elif "hysterical" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Emotions/Positive/Hysterical_1")
                elif "vacuum" in result.lower():
                    nao.behave.startBehavior("animations/Stand/Waiting/Vacuum_1")
                # elif "talk" in result.lower():
                #     nao.behave.startBehavior("animations/SitOnPod/BodyTalk/Speaking/BodyTalk_9")
                # elif "talk2" in result.lower():
                #     nao.behave.startBehavior("animations/Stand/Emotions/Negative/Sorry_1")
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
    
    
    def parse_input(self, input_str):
        # Remove the leading and trailing square brackets
        input_str = input_str.strip('[]')
        # Remove the leading 'u' character if present
        input_str = input_str.replace("u'", "'")
        # Use ast.literal_eval to parse the input string into a dictionary
        data_dict = ast.literal_eval(input_str)

        return data_dict

    def wake_wrd_loop(self, nao, wake):
        while wake and not nao.gpt_request:
            t  = self.client_socket.recv(2048)
            # try:
            result = self.parse_input(str(pickle.loads(t))) #self.process_res_( str(pickle.loads(t)) )
            #print("Wake word Response : \n " , result)
            if result["func"] == "Dance":
                print("------\n")
                print("Dance actions will be executed")
                nao.sayText_no_url( "I will start dancing now" )
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
                
                self.dance_sckt = threading.Thread( target= nao.dance_nao )
                self.play_song_sckt = threading.Thread( target= nao.play_song )

                nao.posture.goToPosture("Stand" , 0.4)
                nao.ledStopListening()

            elif result["func"] == "chat":
                print("------\n")
                print("Aiko will respond to question asked ")
                print(str(result["arg"]))
                try:
                    nao.sayText_no_url( str(result["arg"]) )
                except:
                    nao.sayText_no_url( "Sorry I am not able to process your request for a moment" )
                    #nao_.sayText("Sorry I am not able to process your request for a moment")
                
                nao.posture.goToPosture("Stand" , 0.4)
                nao.ledStopListening()

            elif result["func"] == "map":
                print("------\n")
                print("Map will be displayed")
                print("------\n")
                print(result["arg"])
                nao.sayText_no_url( " I cant show map as I dont have display " )
                # nao.display_givenURL(result["arg"])
                
                nao.posture.goToPosture("Stand" , 0.4)
                nao.ledStopListening()
            
            elif result["func"] == "chat_no_url":
                nao.sayText_no_url( str(result["arg"])  )
                nao.ledStartListening()
                nao.posture.goToPosture("Stand" , 0.4)
            
            elif result["func"] == "Reset":
                # nao.tab_reset()
                # nao.sayText_no_url( "Code has been reset " )
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()
            
            elif result["func"] == "president":
                image_path = "/home/hri/nao_dev/python2/drivers/president.png"
                nao.sayText_no_url( str(result["arg"]) )
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()

            elif result["func"] == "chair":
                image_path = "/home/hri/nao_dev/python2/drivers/chair.png"
                nao.sayText_no_url( str(result["arg"]) )
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()

            elif result["func"] == "provost":
                image_path = "/home/hri/nao_dev/python2/drivers/provost.png"
                nao.sayText_no_url( str(result["arg"]) )
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()

            elif result["func"] == "dean":
                image_path = "/home/hri/nao_dev/python2/drivers/dean.png"
                nao.sayText_no_url( str(result["arg"]) )
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()

            elif result["func"] == "vpr":
                image_path = "/home/hri/nao_dev/python2/drivers/vpr.png"
                nao.sayText_no_url( str(result["arg"]) )
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()
            
            elif result["func"] == "sing":
                nao.behave.startBehavior("animations/Stand/Waiting/HappyBirthday_1")        
                nao.posture.goToPosture("StandInit" , 0.4)
                nao.ledStopListening()

            else:
                nao.sayText_no_url( " Unknown command received, Please try again  " )
                print("------\n")
                print("Error encountered ")
                nao.posture.goToPosture("Stand" , 0.4)
                nao.ledStopListening()

            # except:
            #     #print("Error in getting response")
            #     #return None
            #     nao.sayText( " I encountered some error, Please try again " )
            #     print("------\n")
            #     print(" Some error in try except loop of wake_word socket ")
            #     nao.posture.goToPosture("Stand" , 0.4)
 