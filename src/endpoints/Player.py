from falcon.status_codes import * 
import json
from queue import Queue

def get_player_status() -> dict:
    '''
    Returns the current state of the player. 
    @return dict with keys:
    'playing':Boolean,
    'position':float, Percentage of total media played.
    'length':int, Length of current media being played in miliseconds.
    'volume':int, Interger between 0 and 100 (inclusive) where 0 represents muted, and 100 is 0dB.
    '''
    # player_event_queue.put({'command': 'status', 'args': None})
    # return player_status_queue.queue[0]
    pass

def get_library() -> dict:
    
    
    pass

class player(object):

    def __init__(self, player_events: Queue, status:Queue) -> None:
        self.player_event = player_events
        self.status = status

    def on_get(self, req,  resp):
        resp.status = HTTP_200
        resp.text = json.dumps(())
    
    def on_post(self, req, resp):
        resp.status =  HTTP_200
        try:
            match ((req.media['command']).lower()):
                case 'play':
                    self.player_event.put({'message': 'play', 'data': None})
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
            resp.text = json.dumps({"result": "success"})
        except:
            resp.text = json.dumps({"result": "failure"})