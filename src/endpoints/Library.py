from falcon.status_codes import * 
import json

from entities.Media import MediaLibrary

class library(object):

    def __init__(self, media_library: MediaLibrary) -> None:
        self.media_library = media_library

    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'application/json'
        resp.text = json.dumps({"media": list(self.media_library.libaray.all())})
        #returns an array of all the json serialized items in the media library
    def on_post(self, req, resp):
        temp = req.get_param('media_cover')
        object_methods = [method_name for method_name in dir(req)
                  if callable(getattr(req, method_name))]
        resp.status = HTTP_200
        resp.content_type = 'text/html'
        print(req)
        data = req.get_media()
        body = req.get_param('media_cover')
        local_path = body.filename
        with open(local_path, 'wb') as temp_file:
            temp_file.write(body.file.read())
        resp.text = "hello"
        #Allows deletion of media, uploading of media, adding a given media item to a medialist.  
