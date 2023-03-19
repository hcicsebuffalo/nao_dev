#! /usr/bin/python2
# -*- encoding: UTF-8 -*-

# Hash bang line added at top 

import naoqi
import json
from naoqi import ALProxy
import socket 

# def main():
#   while (1):
#     execute_flag = input("Do you want the code to exit? Yes, press:1 ; No, press:Any key ")
#     if (execute_flag == '1'):
#       return
#     else:
#       continue
#       # create a socket object
#       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#       # get local machine name
#       host = socket.gethostname()

#       port = 9999

#       # connection to hostname on the port.
#       s.connect((host, port))

#       # Receive no more than 1024 bytes
#       data = s.recv(1024)


#       data_string = data.encode()
#       print(data_string)

# if __name__ == "__main__":
#     main()


json_data = open('json_file.json')
data = json.load(json_data)
data_string = data.encode()
NAO_IP = "10.0.107.217"
NAO_PORT = 9559
PEPPER_IP = "10.0.52.247"
PEPPER_PORT = 9503

tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
tts.say(data_string)



# print(data_string)

# tts.say("Hello World")


# print("number2")