import threading
import configparser
import subprocess

def read_config(config):
  # Define the commands to run each script
  script1_cmd = 'bash; conda activate hri; python vision.py'
  script2_cmd = 'bash; conda activate hri; python main3.py'
  script3_cmd = 'bash; conda activate hri; python gui.py'

  if (config['vision']['execute_flag'] == 'True'):
    subprocess.Popen(script1_cmd, shell=True)
    # subprocess.run(['conda', 'run', '-n', 'hri', 'python', 'vision.py'])

  if (config['main3']['execute_flag'] == 'True'):
    subprocess.Popen(script2_cmd, shell=True)
    # subprocess.run(['conda', 'run', '-n', 'hri', 'python', 'main3.py'])

  if (config['gui']['execute_flag'] == 'True'):
    subprocess.Popen(script3_cmd, shell=True)
    # subprocess.run(['conda', 'run', '-n', 'hri', 'python', 'gui.py'])

def rewrite_config():
  #create configparser object0
  config = configparser.ConfigParser()
  config.read('config.ini')

  config.set('vision', 'wait_flag', 'False')
  config.set('gui', 'wait_flag', 'False')













  0
0 0 config.set('main3', 'wait_flag', 'False')
  config.set('main2', 'wait_flag', 'False')

  with open('config.ini', 'w') as configfile:
    config.write(configfile)

def main():
  
  config = configparser.ConfigParser()
  config.read('config.ini')

  # execute the primary modules
  read_config(config)

  # wait for the wait_flag these 3 modules
  while(1):
    # Will read the config file again as the contents might change
    config.read('config.ini')
    if (config['vision']['wait_flag'] == 'True' and 
        config['main3']['wait_flag'] == 'True' and
        config['gui']['wait_flag'] == 'True') :
      # Define the commands to run each script
      script_cmd = 'conda activate hri; python main2.py'      
      subprocess.Popen(script_cmd, shell=True)
      # subprocess.run(['conda', 'run', '-n', 'hri', 'python', 'main2.py'])
      rewrite_config()
      # exit from the loop 
      break 


if __name__ == "__main__":
    main()
