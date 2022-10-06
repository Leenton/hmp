import threading
from queue import Queue
import HTTPHandler
import AudioEventHanlder

if __name__ == '__main__':
    
    audio_events = Queue()
    player_status = Queue(maxsize=1)
    lock = threading.Lock()
    

    #audio event hanlder
    audio_event_handler_thread = threading.Thread(target=AudioEventHanlder.start, args=(audio_events, lock))
    
    #http listner service to allow control of the media player and programme queue via http.
    http_handler_thread = threading.Thread(target=HTTPHandler.start, args=(audio_events,player_status))

    audio_event_handler_thread.start()
    http_handler_thread.start()
    audio_event_handler_thread.join()
    http_handler_thread.join()