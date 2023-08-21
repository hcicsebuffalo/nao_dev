import sys
import configparser
import threading

lock = threading.Lock()

print("The intepreter version is: ", sys.version)

i = 100
while (i > 0):
  print("main3, with the value of i:", i)
  if (i == 70):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('main3', 'wait_flag', 'True')
    with open('config.ini', 'w') as configfile:
      config.write(configfile)
    print("main3, changed config")
  i = i - 1

