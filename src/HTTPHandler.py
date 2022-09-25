from queue import Queue
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

class main():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = "2"

    def on_post(self, req, resp):
        print(req)   
        resp.status = falcon.HTTP_200
        resp.body = "2"

class status(object):
    def on_get(self, req,  resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(get_player_status())

class main(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        print(path.relpath("render/main.html"))
        with open('/Users/leenton/python/hmp/src/render/main.html', 'r') as f:
            resp.body = f.read()

handler = falcon.App()
handler.add_route('/api/status', status())
handler.add_route('/api/command', main())
handler.add_route('/', main())

def start_httphandler(event_queue: Queue,status_queue: Queue) -> None:
    global player_event_queue
    player_event_queue = event_queue
    global player_status_queue
    player_status_queue = status_queue
    with make_server('',80,handler) as httpd:
        httpd.serve_forever()