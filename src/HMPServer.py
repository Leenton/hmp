from time import sleep
from turtle import forward
from MediaItem import MediaItem
from Player import Player
from ProgrammeHandler import get_programme_list
import threading
from LevelsHandler import level_controler



import vlc
from time import sleep

# def play_programmes():
#     queue = get_programme_list()
#     player = MediaPlayer()

#     for programme in queue:
#         if(programme):
#             player.play(programme)
            
#             print("looped!" + str(player.name) + "This is main thread")


if __name__ == '__main__':
    
    #player = MediaPlayer() 

    #Start levels handler that manages volume controls seperate to the main thread and interfaces with both and online and physical device to control levels.
#    levels_controll  = threading.Thread(target=level_controler, args=(player))
#    levels_controll.start()

    #Program obtains a generator of items to play, then loops through the iterable, until it reaches the end and stops. Many need to be threaded? 
#    programme_player  = threading.Thread(target=play_programmes, args=[])
#    programme_player.start()
    player = Player()
    queue = get_programme_list()
    print("executing")
    for programme in queue:
        if(programme):
            print(programme)
            player.play(programme["path"])
            print(player.status())
            print("Sleeping for 10 seconds")
            sleep(0.01)
            print(player.status())
            sleep(10)
            player.set_volume(20)
            print(player.status())
            player.jump(10000,"forward")
            sleep(30)
            
            # player.pause()
            # print("Stopping for 3 seconds")
            # sleep(3)
            # player.resume()
            # print("Resuming for 15 seconds")
            # sleep(15)
            # player.pause()
            # print("Stopping for 3 seconds")
            # sleep(3)
            # player.resume()
            # print("Resuming for 5 seconds")
            # sleep(5)
            # print("Restarting the player")
            # player.restart()
            # print("Hold for 10 seconds to prove succesful")
            # sleep(10)
            # print("End of if statement, itterating to next item")
            # if(player.status()["playing"]):
            #     pass


            #wave_obj = sa.WaveObject.from_wave_file("a file")
            #play = wave_obj.play()
            #play.stop()
            #play.is_playing()
            # sleep(20)
            # print(programme["path"])
            # player.play()
            # sleep(50)
            #player.play(programme)
            
            #print("looped!" + str(player.name) + "This is main thread")
    print("FINISHED LOOP")

    # media = vlc.MediaPlayer("storage/media/MV Jack Stauber - Buttercup.mp3")
    # media.play()
    # test = vlv.media==MediaPlayer()
    # sleep(10)
    # media.pause()
    # sleep(5)
    # media.play()
    # sleep(20)
