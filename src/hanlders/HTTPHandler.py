from queue import Queue
import queue
import falcon
from wsgiref.simple_server import make_server

from time import sleep

from endpoints.Player import *
from endpoints.Config import *
from endpoints.Library import *
from endpoints.Resources import *
from endpoints.Main import *


def start(event_queue: Queue,status_queue: Queue) -> None:

    handler = falcon.App()
    handler.add_route('/api/player', player(event_queue,status_queue))
    handler.add_route('/api/library', library())
    handler.add_route('/config', config())
    handler.add_route('/rsc/{folder}/{filename}', resources())
    handler.add_route('/', main())


    with make_server('',80,handler) as httpd:
        httpd.serve_forever()

#start(queue.Queue(),queue.Queue())