import configparser
import subprocess

# config = configparser.ConfigParser()
# config.read('config.ini')

# # # print(config.sections())
# # print(config['Address']['Village'])


# config.set('vision', 'wait_flag', 'True')

# with open('config.ini', 'w') as configfile:
#   config.write(configfile)


subprocess.Popen(['python main2.py'], shell= True)
subprocess.Popen(['python gui.py'] , shell= True)