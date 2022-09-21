import random
from sre_constants import JUMP
from time import sleep
from turtle import position
import vlc

class Player:
    
    def __init__(self) -> None:
        self.name = random.randint(1000,10000000)
        self.media_player = vlc.MediaPlayer()
        self.current_item = None
    
    def play(self,media: str) -> None:
        '''
        @param media:str, file path to the media item you wannt to play.
        '''
        self.current_item = media
        self.media_player.set_media(vlc.Media(self.current_item))
        self.media_player.play()
    
    def pause(self) -> None:
        '''
        Pauses the player and stops playing audio. 
        '''
        self.media_player.pause()
    
    def resume(self) -> None:
        '''
        Resumes playing the current item the player had when it was paused.
        '''
        if self.current_item and self.status()["playing"] == False:
            self.media_player.play()

    def restart(self) -> None:
        '''
        Restarts the current item the player has from the begining of the media file. 
        '''
        self.play(self.current_item)
    
    def jump(self, distance: int, direction: str):
        '''
        Skips the playhead of the player to another point in the current media being played. 
        @param distance:int, Integer presenting how many miliseconds you want to move the playhead.
        @param direction:str, String either 'forward' or 'back' to represent which direct you want to move the playhead.
        '''
        status = self.status()
        
        if self.current_item:
            distance = distance / status["length"]
            
            if direction =="forward":
                position = status["position"] + distance
                if position > 1:
                    position = 1
            elif direction == "back":
                position = status["position"] - distance
                if position < 0:
                    position = 0

            self.media_player.set_position(position)

    def status(self) -> dict:
        '''
        Returns the current state of the player object. 
        @return dict with keys:
        'playing':Boolean,
        'position':float, Percentage of total media played.
        'length':int, Length of current media being played in miliseconds.
        'volume':int, Interger between 0 and 100 (inclusive) where 0 represents muted, and 100 is 0dB.
        '''
        status = {}

        if self.media_player.is_playing():
            status["playing"] = True
            status["position"] = self.media_player.get_position()
            status["length"] = self.media_player.get_length()
            status["volume"] = self.media_player.audio_get_volume()
        else:
            status["playing"] = False
            status["position"] = None
            status["length"] = 0
            status["volume"] = self.media_player.audio_get_volume()

        return status

    def set_volume(self, level: int) -> None:
        '''
        Set the volume of the audio player back. 
        @param level:int, Interger between 0 and 100 (inclusive) where 0 represents muted, and 100 is 0dB.
        '''
        if not(level < 0 or level > 100):
            self.media_player.audio_set_volume(level)
            self.volume = level



