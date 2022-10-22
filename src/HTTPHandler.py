from ast import match_case
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

class player():
    def on_get(self, req,  resp):
        resp.status = falcon.HTTP_200
        resp.text = json.dumps(get_player_status())
    
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        try:
            match ((req.media['command']).lower()):
                case 'play':
                    player_event_queue.put({'message': 'play', 'data': None})
                case 'pause':
                    player_event_queue.put({'message': 'pause', 'data': None})
                case 'resume':
                    player_event_queue.put({'message': 'resume', 'data': None})
                case 'restart':
                    player_event_queue.put({'message': 'restart', 'data': None})
                case 'back':
                    player_event_queue.put({'message': 'jump', 'data': [5000, 'back']})
                case 'backback':
                    player_event_queue.put({'message': 'jump', 'data': [20000, 'back']})
                case 'forward':
                    player_event_queue.put({'message': 'jump', 'data': [5000, 'forward']})
                case 'forwardforward':
                    player_event_queue.put({'message': 'jump', 'data': [20000, 'forward']})
            resp.text = json.dumps({"result": "success"})
        except:
            resp.text = json.dumps({"result": "failure"})

class library(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #returns an array of all the json serialized items in the media library
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #Allows deletion of media, uploading of media, adding a given media item to a medialist.  

class playlists(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #returns an array of all the json serialized items in the media list
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = "hello"
        #Allows deletion of media lists, creating new lists, removing items from a list. Setting playback types and etc.  

class config(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        print(path.relpath("render/config.html"))
        with open('/Users/leenton/python/hmp/src/web/config.html', 'r') as f:
            resp.text = f.read()
          
class main(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        print(path.relpath("render/main.html"))
        with open('/Users/leenton/python/hmp/src/web/main.html', 'r') as f:
            resp.text = f.read()

class resources(object):
    def on_get(self,req, resp, folder, filename):
        resp.status = falcon.HTTP_200
        #logic to check what the file extension is and to set the correct header based on the file type. 
        file_format = (filename.split('.'))[-1]
        match (file_format):
            case 'css':
                resp.content_type = 'text/css'
            case 'htm':
                resp.content_type = 'text/html'
            case 'html':
                resp.content_type = 'text/html'
            case 'jpg':
                resp.content_type = 'image/jpg'
            case 'png':
                resp.content_type = 'image/png'
            case 'gif':
                resp.content_type = 'image/gif'
            case 'ttf':
                resp.content_type = 'image/ttf'
        with open('/Users/leenton/python/hmp/src/web/rsc/' + folder + '/' + filename, 'rb') as f:
            resp.text = f.read()
        

handler = falcon.App()
handler.add_route('/api/player', player())
handler.add_route('/api/library', library())
handler.add_route('/config', config())
handler.add_route('/rsc/{folder}/{filename}', resources())
handler.add_route('/', main())

def start(event_queue: Queue,status_queue: Queue) -> None:
    global player_event_queue
    player_event_queue = event_queue
    global player_status_queue
    player_status_queue = status_queue
    with make_server('',80,handler) as httpd:
        httpd.serve_forever()

start(queue.Queue(),queue.Queue())