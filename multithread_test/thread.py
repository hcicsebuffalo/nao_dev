import threading
import configparser

def run_file(file_name):
  exec(open(file_name).read())


def null_thread():
  pass

def read_config(config):
  # config = configparser.ConfigParser()
  # config.read('config.ini')

  # Assigning null threads
  thread1 = threading.Thread(target=null_thread)
  thread2 = threading.Thread(target=null_thread)
  thread3 = threading.Thread(target=null_thread)
  thread4 = threading.Thread(target=null_thread)

  if (config['vision']['execute_flag'] == 'True'):
    thread1 = threading.Thread(target = run_file, args=("vision.py",))

  if (config['main3']['execute_flag'] == 'True'):
    thread3 = threading.Thread(target = run_file, args=("main3.py",))

  if (config['gui']['execute_flag'] == 'True'):
    thread2 = threading.Thread(target = run_file, args=("gui.py",))

  thread1.start()
  thread2.start()
  thread3.start()

  thread1.join()
  thread2.join()
  thread3.join()

def rewrite_config():
  #create configparser object
  config = configparser.ConfigParser()
  config.read('config.ini')

  config.set('vision', 'wait_flag', 'False')
  config.set('gui', 'wait_flag', 'False')
  config.set('main3', 'wait_flag', 'False')
  config.set('main2', 'wait_flag', 'False')

  with open('config.ini', 'w') as configfile:
    config.write(configfile)
  # #define sections and their key and value pairs
  # config["vision"]={
  #         "execute_flag": "True",
  #         "wait_flag": "False",
  #         }
  # config["gui"]={
  #         "execute_flag":"True",
  #         "wait_flag" : "False"
  #         }
  # config["main3"]={
  #         "execute_flag": "True",
  #         "wait_flag": "False"
  #         }
  # config["main2"]={
  #         "execute_flag": "True",
  #         "wait_flag": "False"
  #         }
  
  # #SAVE/REWRITE CONFIG FILE
  # with open("config.ini","w") as file_object:
  #     config.write(file_object)
  # print("Config file 'config.ini' created")

def main():
  
  config = configparser.ConfigParser()
  config.read('config.ini')

  # execute the primary modules
  read_config(config)

  # wait for the wait_flag these 3 modules
  while(1):
    # Will read the config file again as the contents might change
    # print("Inside the while condition")
    config.read('config.ini')
    # if (config['vision']['wait_flag'] == 'True' and 
    #     config['gui']['wait_flag'] == 'True' and
    #     config['main3']['wait_flag'] == 'True') :
    if (config['vision']['wait_flag'] == 'True' and 
        config['main3']['wait_flag'] == 'True' and
        config['gui']['wait_flag'] == 'True') :
      thread4 = threading.Thread(target = run_file, args=("main2.py",))
      thread5 = threading.Thread(target = rewrite_config)
      
      thread4.start()
      thread5.start()

      thread4.join()
      thread5.join()

      # exit from the loop 
      break 


if __name__ == "__main__":
    main()




# thread1 = threading.Thread(target=run_file, args=("first.py",))
# thread2 = threading.Thread(target=run_file, args=("second.py",))

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

 
# #create configparser object
# config_file = configparser.ConfigParser()
 
# #define sections and their key and value pairs
# config_file["Address"]={
#         "Name": "Aditya Raj",
#         "Village": "Bhojpur",
#         "District": "Samastipur",
#         "State": "Bihar"
#         }
# config_file["Education"]={
#         "College":"IIITA",
#         "Branch" : "IT"
#         }
# config_file["Favorites"]={
#         "Sports": "VolleyBall",
#         "Books": "Historical Books"
#         }
 
# #SAVE CONFIG FILE
# with open("config.ini","w") as file_object:
#     config_file.write(file_object)
# print("Config file 'config.ini' created")
 
# #print file content
# read_file=open("config.ini","r")
# content=read_file.read()
# print("content of the config file is:")
# print(content)