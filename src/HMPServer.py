import threading
from queue import Queue
from time import sleep
from Player import Player
from ProgrammeHandler import get_programme_list


def play_programmes(player_event_queue: Queue, player_status_queue: Queue):
    #helper function to check player status. 
    def get_player_status(q: Queue) -> dict:
        '''
        Returns the current state of the player. 
        @return dict with keys:
        'playing':Boolean,
        'position':float, Percentage of total media played.
        'length':int, Length of current media being played in miliseconds.
        'volume':int, Interger between 0 and 100 (inclusive) where 0 represents muted, and 100 is 0dB.
        '''
        player_event_queue.put({'command': 'status', 'args': None})
        sleep(0.1)
        return player_status_queue.queue[0]

    while(True):    
        programme_queue = get_programme_list()
        for programme in programme_queue:
            if(programme):
                #Tell the player to play the chosen programme.
                player_event_queue.put({'command': 'play', 'args': programme['path']})

                #Sleep for 0.5 seconds to allow the player to load the file form storage and begin playing. 
                sleep(0.5)

                #while the player is playing the programme, sleep and wait for it to end.
                while((get_player_status(player_status_queue))['playing'] or (get_player_status(player_status_queue))['paused'] ):
                    sleep(1)
        sleep(0.5)

def PlayerEventHandler(event_queue: Queue, status_queue: Queue):
    #get an instance of the player object we will be using to play programmes.
    player = Player()

    #Check the player event queue forever, execute the correct command for the coresponding event.
    running = True
    while(running):
        event = event_queue.get()
        event_queue.task_done()
        if(event):
            match (event['command']):
                case 'play':
                    player.play(event['args'])

                case 'pause':
                    player.pause()

                case 'resume':
                    player.resume()

                case 'restart':
                    player.restart()

                case 'jump':
                    player.jump(event['args'][0], event['args'][1])

                case 'status':
                    with lock:
                        status = player.status()
                        if(status_queue.empty()):
                            status_queue.put(status)
                        else:
                            val = status_queue.get()
                            status_queue.task_done()
                            del val
                            status_queue.put(status)
                    
                case 'status2':
                    status = player.status()
                    print(status)
                    print(status_queue.queue[0])

                case 'set_volume':
                    player.set_volume(event['args'])
                case 'kill':
                    running = False
        sleep(0.1)              

if __name__ == '__main__':
    
    player_event_queue = Queue()
    player_status = Queue(maxsize=1)
    lock = threading.Lock()
    
    #player event hanlder that controls the player
    player_thread = threading.Thread(target=PlayerEventHandler, args=(player_event_queue,player_status))

    #programme queue that controls what should be played.
    programming_thread = threading.Thread(target=play_programmes, args=(player_event_queue,player_status))

    
    player_thread.start()
    programming_thread.start()

    while(True):
        command = input("What do you want the player to do? ")
        args = input("What args are you sending? ")
        player_event_queue.put({'command':command, 'args': args})


    player_thread.join()
    programming_thread.join()
