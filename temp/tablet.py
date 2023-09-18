from naoqi import ALProxy
import time

#from python2.animations import *

ip = "10.0.255.8"
port = 9559

tabletService = ALProxy("ALTabletService" , ip, port)

try:

    # Ensure that the tablet wifi is enable
    tabletService.enableWifi()

    # Display a web page on the tablet
    tabletService.showWebview("http://www.google.com")

    time.sleep(3)

    # Display a local web page located in boot-config/html folder
    # The ip of the robot from the tablet is 198.18.0.1
    #tabletService.showWebview("http://198.18.0.1/apps/boot-config/preloading_dialog.html")

    time.sleep(3)

    # Hide the web view
    tabletService.hideWebview()
except Exception:
    print ("Error was: ")