from MediaPlayer import MediaPlayer
from ProgrammeHandler import get_programme_list
import threading
from LevelsHandler import level_controler

def play_programmes():
    queue = get_programme_list()
    player = MediaPlayer()

    for programme in queue:
        if(programme):
            player.play(programme)
            
            print("looped!" + str(player.name) + "This is main thread")


if __name__ == '__main__':
    
    player = MediaPlayer() 

    #Start levels handler that manages volume controls seperate to the main thread and interfaces with both and online and physical device to control levels.
    levels_controll  = threading.Thread(target=level_controler, args=(player))
    levels_controll.start()

    #Program obtains a generator of items to play, then loops through the iterable, until it reaches the end and stops. Many need to be threaded? 
    programme_player  = threading.Thread(target=play_programmes, args=[])
    programme_player.start()


