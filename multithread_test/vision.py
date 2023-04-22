import sys
import configparser
import threading

lock = threading.Lock()

print("The intepreter version is: ", sys.version)

i = 100
while (i > 0):
  print("VISION, with the value of i:", i)
  if (i == 70):
    with lock:
      config = configparser.ConfigParser()
      config.read('config.ini')
      config.set('vision', 'wait_flag', 'True')
      with open('config.ini', 'w') as configfile:
        config.write(configfile)
      print("VISION, changed config")
  i = i - 1


