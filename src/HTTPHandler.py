from queue import Queue
import queue
import falcon
from wsgiref.simple_server import make_server
import json
from time import sleep
from os import path

player_event_queue = None
player_status_queue = None

def get_player_status() -> dict:
    '''
    Returns the current state of the player. 
    @return dict with keys:
    'playing':Boolean,
    'position':float, Percentage of total media played.
    'length':int, Length of current media being played in miliseconds.
    'volume':int, Interger between 0 and 100 (inclusive) where 0 represents muted, and 100 is 0dB.
    '''
    player_event_queue.put({'command': 'status', 'args': None})
    return player_status_queue.queue[0]

class test():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"Value": "wdkjjkqhwdkjqwqlwkjdhqwkljdhqwkljedhqwlkejdh"})

class player():
    def on_get(self, req,  resp):
        resp.status = falcon.HTTP_200
        resp.text = json.dumps(get_player_status())
    
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        try:
            match ((req.media['command']).lower()):
                case 'play':
                    player_event_queue.put({'command': 'play', 'args': None})
                case 'pause':
                    player_event_queue.put({'command': 'pause', 'args': None})
                case 'resume':
                    player_event_queue.put({'command': 'resume', 'args': None})
                case 'restart':
                    player_event_queue.put({'command': 'restart', 'args': None})
                case 'back':
                    player_event_queue.put({'command': 'jump', 'args': [5000, 'back']})
                case 'backback':
                    player_event_queue.put({'command': 'jump', 'args': [20000, 'back']})
                case 'forward':
                    player_event_queue.put({'command': 'jump', 'args': [5000, 'forward']})
                case 'forwardforward':
                    player_event_queue.put({'command': 'jump', 'args': [20000, 'forward']})
            resp.text = json.dumps({"result": "success"})
        except:
            resp.text = json.dumps({"result": "failure"})



class main(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        print(path.relpath("render/main.html"))
        with open('/Users/leenton/python/hmp/src/render/main.html', 'r') as f:
            resp.body = f.read()

handler = falcon.App()
handler.add_route('/api/player', player())
handler.add_route('/api/test', test())
handler.add_route('/', main())

def start_httphandler(event_queue: Queue,status_queue: Queue) -> None:
    global player_event_queue
    player_event_queue = event_queue
    global player_status_queue
    player_status_queue = status_queue
    with make_server('',80,handler) as httpd:
        httpd.serve_forever()

#start_httphandler(queue.Queue(),queue.Queue())