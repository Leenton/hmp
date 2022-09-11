from os.path import exists

class MediaItem():
    def __init__(self,file_path: str, media_type: str, name = None, ) -> None:
        #set obtain the name of the file.
        self.file_name = file_path.split('/')[-1]
        
        #set the name of the media item to that specified or just the name of the file without the file extension
        if(name):
            self.name = name
        else: 
            self.name = file_path.split('/')[-1][0:(self.file_name.rindex("."))]

        #Set the media type to either Podcast,String
        match (media_type.lower()):
            case "music":
                self.media_type = "music"
                self.playbacktype = "loop"
            case "podcast":
                self.media_type = "podcast"
                self.playbacktype = "once"
            case "weather":
                self.media_type = "weather"
                self.playbacktype = "loop"
        
        #The rank determins how likely a media item is to be chosen when determining the next piece of media to play. 
        self.rank = 0
        
        #Set the cover art for the music file being played. 
        if(exists(("./../storage/covers/" + self.name + ".png"))):
            self.cover_art = "./../storage/covers/" + self.name + ".png"
        else:
            self.cover_art = "./../storage/covers/default.png"