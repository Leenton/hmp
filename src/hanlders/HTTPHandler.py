from queue import Queue
from sched import scheduler
from threading import Lock
from falcon import App
import falcon.asgi
import falcon.media
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


# class SomeMiddleware:
#     async def process_request_ws(self, req: Request, ws: WebSocket):
#         # This will be called for the HTTP request that initiates the
#         #   WebSocket handshake before routing.
#         pass

#     async def process_resource_ws(self, req: Request, ws: WebSocket, resource, params):
#         # This will be called for the HTTP request that initiates the
#         #   WebSocket handshake after routing (if a route matches the
#         #   request).
#         pass

def start(event_queue: Queue,status_queue: Queue, lock: Lock) -> None:

    handler = App(middleware=MultipartMiddleware())
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