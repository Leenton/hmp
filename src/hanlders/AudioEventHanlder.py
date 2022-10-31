from queue import Queue
from threading import Lock
from entities.Player import Player, PlayerState
import asyncio
from entities.Media import MediaItem, MediaLibrary, MediaList


async def status_hanlder(event_queue: Queue, lock: Lock):
    while True:
        with lock:
            status = player.status()
            event_queue.put({'message': 'status_update', 'data':status })
        await asyncio.sleep(0.5)

async def audio_event_loop(event_queue: Queue, lock: Lock):
    #create an event to play the first item we get form the play list iterator 
    task = asyncio.create_task(status_hanlder(event_queue, lock))
    while True:
        #Check if a new event has been created, and if so process it acordingly. 
        try:
            event = event_queue.get(block=False)
            if(event):
                with lock:
                    if(event['data']):
                        eval('on_' + event['message'] + '(' + 'event["data"]' +')')
                    else: 
                        eval('on_' + event['message'] + '()')
        except:
            await asyncio.sleep(0.01)
        
def start(audio_event_queue: Queue, lock: Lock):
    global player
    global library
    global playlist
    global event_queue

    event_queue = audio_event_queue
    
    with lock:
        player = Player()
        library = MediaLibrary()
    
    playlist = iter(library.get_media_list("main"))
    
    #playlist = get_programme_list()
    
    item = next(playlist)
    event_queue.put({"message": "play", "data": item })
    
    asyncio.run(audio_event_loop(event_queue, lock))

def on_play(event: MediaItem | MediaList) -> None:
    global playlist
    if isinstance(event, MediaList):
        playlist = iter(event)
        event = next(player)

    player.play(event)
    #update anyone who is subscribed to this that the audio player has changed. 

def on_pause() -> None:
    player.pause()
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_resume() -> None:
    player.resume()
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_restart() -> None:
    player.restart()
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_set_volume(event) -> None:
    player.set_volume(event)
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_jump(event: list) -> None:
    player.jump(event[0], event[1])
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_media_end(media) -> None:
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_media_start() -> None:
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_play_next() -> None:
    next_media = next(playlist)
    if(next_media):
        player.play(next_media)
    else:
        player.set_inactive()
    
def on_play_previous() -> None:
    #make an event to play and send the previous item from the generator
    pass

def on_status_update(status: dict) -> None:
    if(status['state'] is PlayerState.Finished or status['state'] is PlayerState.Inactive):
        if(status['state'] is PlayerState.Finished):
            event_queue.put({'message': 'media_end', 'data': status})
        event_queue.put({'message': 'play_next', 'data': None})

def on_kill():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass




#start(Queue(), Lock())
