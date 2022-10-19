import threading
from queue import Queue
import HTTPHandler
import AudioEventHanlder

if __name__ == '__main__':
    
    audio_events = Queue()
    media_events = Queue()
    player_status = Queue(maxsize=1)
    lock = threading.Lock()

    #audio event hanlder
    audio_event_handler_thread = threading.Thread(target=AudioEventHanlder.start, args=(audio_events, lock))
    
    #http listner service to allow control of the media player and programme queue via http.
    http_handler_thread = threading.Thread(target=HTTPHandler.start, args=(audio_events,player_status))

    #physical IO handler to handle any physical inputs we recieve from the real worl. 
    #physical_io_handler_thread = threading.Thread(target=PhysicalIOHandler.start, args=(audio_events,player_status))

    #Media handler to handle loading of jsons, and . 
    #media_handler_thread = threading.Thread(target=MediaHanlder.start, args=(media_events))

    audio_event_handler_thread.start()
    http_handler_thread.start()

    '''
    
    Some more complex actions happen in the main thread, such as picking when to trigger the downloader
    Deciding how to change the levels and follow the strict schedule for when thing sould play and etc

    the main thread is the scheudler that instructs all the other event threads what to do. By creating events for 
    them to process. 

    '''
    
    audio_event_handler_thread.join()
    http_handler_thread.join()