from concurrent.futures import thread
from queue import Queue
import queue
from threading import Lock
import threading
from time import sleep
from Player import Player
import asyncio

event = {}

def on_play():
    player.play(event['args'])
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

def on_set_volume():
    player.set_volume(event['args'])
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_jump():
    player.jump(event['args'][0], event['args'][1])
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_song_end():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_song_start():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

def on_play_next():
    #make an event to play, and send the next item from the generator
    pass

def on_play_previous():
    #make an event to play and send the previous item from the generator
    pass

def on_kill():
    #update anyone who is subscribed to this that the audio player has changed. 
    pass

async def status_hanlder(audio_events: Queue, lock: Lock):
    while True:
        with lock:
            status = player.status()
        audio_events.put(status)
        await asyncio.sleep(0.5)

async def audio_event_loop(audio_events: Queue, lock: Lock):

    #create an event to play the first item we get form the play list iterator 
    task = asyncio.create_task(status_hanlder(audio_events, lock))
    while True: 
        #Check if a new event has been created, and if so process it acordingly. 
        try:
            event = audio_events.get(block=False)
            if(event):
                with lock:
                    eval('on_' + event + '()')
        except:
            await asyncio.sleep(0.01)
        
def start(audio_events: Queue, lock: Lock):
    
    global player
    global playlist
    player = Player()
    playlist = []

    asyncio.run(audio_event_loop(audio_events, lock))

start(Queue(), Lock())