from hanlders.HTTPHandler import start
from queue import Queue
from threading import Lock

start(Queue(),Queue(), Lock())