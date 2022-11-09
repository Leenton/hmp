from falcon.status_codes import * 
import json

from entities.Media import MediaLibrary
from entities.Media import MediaItem
from HMPConfig import *
class library(object):

    def __init__(self, media_library: MediaLibrary) -> None:
        self.media_library = media_library
    
    def on_get(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'application/json'
        resp.text = json.dumps({"media": list(self.media_library.libaray.all())})
        #returns an array of all the json serialized items in the media library
    def on_post(self, req, resp):
        resp.status = HTTP_200
        resp.content_type = 'text/html'
        params = req.get_media()

        #if the request is a delete request just remove the media item from the db other wise. 
        if(params['req_type'] == 'delete'):
            self.media_library.remove_media_item(params['media_id'])
        
        if(params['req_type'] == 'edit'):
            item = MediaItem(
                params['media_file'],
                params['media_name'],
                params['media_id'],
                params['media_type'],
                params['media_created'],
                params['media_cover'],
            )
            self.media_library.update_media_item(item)

            #To edit, we just build the media item from the new data we were given, get the rest of the data from the media item in the library
            #remove the old media item from memory, then we just insert the new media item into the library
            #Bish bash bosh we done, we could maybe create a whole as method in the library to account for updating, but honestly I think this is probably fine, 
            #I don't think it's probably fine as we will have to do this multiple times, and this logic will get messy over time if gave to reimplemet this over
            #and over. so I am in favour of just creating an update media item method, that takes a media id, and the data from the new fields, sounds, simpler
            #at least for me to interact with it. 
            #execute logic to ammend the given media item 
            pass

        if(params['req_type'] == 'upload'):
            #Create a new media item. 
            new_item = MediaItem(
                params['media_file'],
                params['name'],
                None,
                params['media_type'],
                None,
                (params["media_cover"] if params["media_cover"] else (DEFAULT_COVERS + params['media_cover'] + '.png')),
            )
            #Get the media file from the request.
            if(params['media_file']):
                body = req.get_param('media_file')
                local_path = COVER_IMAGES + body.filename
                with open(local_path, 'wb') as temp_file:
                    temp_file.write(body.file.read())
                #move the file to the configured media store. 
            
            if(params['media_cover']):
                body = req.get_param('media_cover')
                local_path = MEDIA_FILES + body.filename
                with open(local_path, 'wb') as temp_file:
                    temp_file.write(body.file.read())
                #move the file to the configured media store. 

            self.media_library.insert_media_item(new_item)
        
        resp.text = '{"result":"success"}'
