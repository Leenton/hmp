import vlc
from enum import Enum
from hanlders.HTTPHandler import player
from entities.Media import MediaItem


from time import sleep
import traceback
import sys

class PlayerState(Enum):
    Inactive = 'Inactive'
    Playing = 'Playing'
    Paused = 'Paused'
    Finished = 'Finished'

class Player:
    
    def __init__(self) -> None:
        self.media_player = vlc.MediaPlayer()
        self.state = PlayerState.Inactive
        self.position = 0 
        self.length = 0 
        self.volume = 100
        self.current_media = MediaItem("","")
    
    def play(self,media: MediaItem) -> None:
        '''
        TO DO
        '''
        self.current_media = media
        self.media_player.set_media(vlc.Media(self.current_media.path))
        self.media_player.play()
        sleep(0.5)
        self.length = self.media_player.get_length()
        self.state = PlayerState.Playing
    
    def pause(self) -> None:
        '''
        Pauses the player and stops playing audio. 
        '''
        self.media_player.pause()
        self.state = PlayerState.Paused
    
    def resume(self) -> None:
        '''
        Resumes playing the current item the player had when it was paused.
        '''
        if self.current_media and self.state == PlayerState.Paused:
            self.media_player.play()
            self.state = PlayerState.Playing
    
    def set_inactive(self) -> None: 
        '''
        TO DO 
        '''
        self.state = PlayerState.Inactive
        self.position = 0 
        self.length = 0 
        self.current_media = MediaItem("","")

    def restart(self) -> None:
        '''
        Restarts the current media item the player has from the begining of the media file. 
        '''
        self.play(self.current_media)
    
    def jump(self, distance: int, direction: str):
        '''
        Skips the playhead of the player to another point in the current media being played. 
        @param distance:int, Integer presenting how many miliseconds you want to move the playhead.
        @param direction:str, String either 'forward' or 'back' to represent which direct you want to move the playhead.
        '''
        print("jump called")
        if self.current_media:
            distance = distance / self.length

            if direction =="forward":
                position = self.position + distance
                if position > 1:
                    position = 1

            elif direction == "back":
                position = self.position - distance
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
        #figure out if we are playing, if we have just ended and etc. 

        if not self.media_player.is_playing() and self.state is PlayerState.Playing and self.position > 0.975:
            self.state = PlayerState.Finished
            self.position = 1

        if self.state is PlayerState.Playing:
            self.position = self.media_player.get_position()

        status = {
            'state': self.state,
            'position': self.position,
            'volume': self.volume,
            'media_name': self.current_media.name,
            'media_id': self.current_media.id,
            'plays': self.current_media.plays,
            'rank': self.current_media.rank,
            'runtime': self.current_media.runtime
        }
        return status



    def set_volume(self, level: int) -> None:
        '''
        Set the volume of the audio player back. 
        @param level:int, Interger between 0 and 100 (inclusive) where 0 represents muted, and 100 is 0dB.
        '''
        if not(level < 0 or level > 100):
            self.media_player.audio_set_volume(level)
            self.volume = level
