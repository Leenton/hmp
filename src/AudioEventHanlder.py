from queue import Queue
from threading import Lock
from Player import Player, PlayerState
import asyncio
from ProgrammeHandler import get_programme_list
from time import sleep
import traceback
import sys

def on_play(event):
    player.play(event)
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_pause():
    player.pause()
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_resume():
    player.resume()
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_restart():
    player.restart()
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_set_volume(event):
    player.set_volume(event['data'])
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_jump(event):
    player.jump(event['data'][0], event['data'][1])
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_song_end():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_song_start():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_play_next():
    next_media = next(playlist)
    if(next_media):
        player.play(next_media)
    else:
        player.set_inactive()
    #make an event to play, and send the next item from the generator
    

def on_play_previous():
    #make an event to play and send the previous item from the generator
    pass

def on_status_update(status):
    if(status['state'] is PlayerState.Finished):
        event_queue.put({'message': 'play_next', 'data': None})
    print(status)
    #raise Exception("Sorry, no numbers below zero")
    #update anyone who is subscribed to this that the audio player has changed. 

def on_kill():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

async def status_hanlder(event_queue: Queue, lock: Lock):
    while True:
        with lock:
            status = player.status()
            event_queue.put({'message': 'status_update', 'data':status })
            print(status)
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
    global playlist
    global event_queue

    event_queue = audio_event_queue
    player = Player()
    playlist = get_programme_list()
    item = next(playlist)
    event_queue.put({"message": "play", "data": item })
    
    asyncio.run(audio_event_loop(event_queue, lock))


start(Queue(), Lock())
