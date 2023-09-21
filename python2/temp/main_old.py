from python2.temp.helper_old import *

import pika

# Open a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
rabbit_channel = connection.channel()
rabbit_channel.queue_declare(queue='py2_py3_queue')
rabbit_channel.queue_declare(queue='gui_queue')

# Initialise nao class
initialise_nao()

# Nao startup routine
nao_startup_routine()

# Attach nao's thread funtions
attach_thread_functions()

# Attach GUI, touch isr and wake_word thread

#GUI_Thread =        threading.Thread(target= nao.socket_loop     , args=(nao , True)                                    )
Touch_ISR =         threading.Thread(target= nao.initTG          , args=(Touch_interrupts, nao, dance, play_song, led)  )
#Wake_Word_Thread =  threading.Thread(target= nao.wake_wrd_loop   , args=(nao , True)                                    )

rabbit_channel.basic_consume(queue='py2_py3_queue', on_message_callback= callback_wake_Wrd, auto_ack=True)
rabbit_channel.basic_consume(queue='gui_queue', on_message_callback= callback_gui, auto_ack=True)

# Start
Touch_ISR.start()
#GUI_Thread.start()
#Wake_Word_Thread.start()
rabbit_channel.start_consuming()