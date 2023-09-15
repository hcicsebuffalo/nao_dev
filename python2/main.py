from helper import *

# Initialise nao class
initialise_nao()

# Nao startup routine
nao_startup_routine()

# Attach nao's thread funtions
attach_thread_functions()

# Attach GUI, touch isr and wake_word thread

GUI_Thread =        threading.Thread(target= nao.socket_loop     , args=(nao , True)                                    )
Touch_ISR =         threading.Thread(target= nao.initTG          , args=(Touch_interrupts, nao, dance, play_song, led)  )
Wake_Word_Thread =  threading.Thread(target= nao.wake_wrd_loop   , args=(nao , True)                                    )

# Start
Touch_ISR.start()
GUI_Thread.start()
Wake_Word_Thread.start()

