from falcon.status_codes import * 
import json
from entities.Media import MediaLibrary
class playlists(object):
    def __init__(self, media_library: MediaLibrary) -> None:
        self.media_library = media_library
        

    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'application/json'
        resp.text = json.dumps({"media_lists": list(self.media_library.lists.all())})
        #returns an array of all the json serialized items in the media list
    def on_post(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #Allows deletion of media lists, creating new lists, removing items from a list. Setting playback types and etc.  