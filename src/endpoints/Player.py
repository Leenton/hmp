from falcon.status_codes import * 
import json
from queue import Queue
from entities.Media import MediaLibrary, MediaItem

class player(object):
    def __init__(self, player_events: Queue, status:Queue, media_library: MediaLibrary) -> None:
        self.player_event = player_events
        self.status = status
        self.media_library = media_library

    # def on_websocket(self, req, ws):
    #     print("fuck")
    #     pass

    def on_get(self, req,  resp):
        resp.status = HTTP_200
        resp.text = json.dumps(())
        print("wrong fuck")
    
    def on_post(self, req, resp):
        try:
            match ((req.media['command']).lower()):
                case 'play':
                    print(req.media)
                    
                    if(req.media["data"]):
                        if(req.media["data"]["type"] == "media"):
                            print("HI")
                            data = self.media_library.get_media_item(req.media["data"]["resouce_id"])
                            print("noo")
                        else:
                            data = self.media_library.get_media_list(req.media["data"]["resouce_id"])

                    else: 
                        data = None
                    
                    self.player_event.put({'message': 'play', 'data': data})
                case 'pause':
                    self.player_event.put({'message': 'pause', 'data': None})
                case 'resume':
                    self.player_event.put({'message': 'resume', 'data': None})
                case 'restart':
                    self.player_event.put({'message': 'restart', 'data': None})
                case 'back':
                    self.player_event.put({'message': 'jump', 'data': [5000, 'back']})
                case 'backback':
                    self.player_event.put({'message': 'jump', 'data': [20000, 'back']})
                case 'forward':
                    self.player_event.put({'message': 'jump', 'data': [5000, 'forward']})
                case 'forwardforward':
                    self.player_event.put({'message': 'jump', 'data': [20000, 'forward']})
            
            resp.status =  HTTP_200
            resp.text = json.dumps({"result": "success"})
        except:
            resp.status = HTTP_500
            resp.text = json.dumps({"result": "failure"})