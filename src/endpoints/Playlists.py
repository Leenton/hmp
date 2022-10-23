from falcon.status_codes import * 
import json

class playlists(object):
    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'application/json'
        resp.text = json.dumps({"result": "success"})
        #returns an array of all the json serialized items in the media list
    def on_post(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #Allows deletion of media lists, creating new lists, removing items from a list. Setting playback types and etc.  