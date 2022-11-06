from queue import Queue
from sched import scheduler
from threading import Lock
import falcon
from wsgiref.simple_server import make_server
from falcon_multipart.middleware import MultipartMiddleware
from endpoints.Player import *
from endpoints.Config import *
from endpoints.Library import *
from endpoints.Playlists import *
from endpoints.Resources import *
from endpoints.Main import *
from endpoints.Scheduler import * 
from entities.Media import MediaLibrary


def start(event_queue: Queue,status_queue: Queue, lock: Lock) -> None:

    handler = falcon.App(middleware=[MultipartMiddleware()])
    with lock:
        media_library = MediaLibrary()


    handler.add_route('/api/player', player(event_queue,status_queue, media_library))
    handler.add_route('/api/library', library(media_library))
    handler.add_route('/api/playlists', playlists(media_library))
    handler.add_route('/api/scheduler', scheduler(media_library))
    handler.add_route('/config', config())
    handler.add_route('/rsc/{folder}/{filename}', resources())
    handler.add_route('/', main())


    with make_server('',80,handler) as httpd:
        httpd.serve_forever()