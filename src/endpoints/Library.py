from falcon.status_codes import * 
import json

from entities.Media import MediaLibrary

class library(object):

    def __init__(self, media_library: MediaLibrary) -> None:
        self.media_library = media_library

    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'application/json'
        resp.text = json.dumps({"result": "success"})
        #returns an array of all the json serialized items in the media library
    def on_post(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #Allows deletion of media, uploading of media, adding a given media item to a medialist.  
