import json
from os import path
from os.path import exists
import json
from enum import Enum
from hashlib import sha1
from time import time

class MediaItemType(Enum):
    Music = 'music'
    Podcast = 'podcast'
    Weather = 'weather'
    Effect = 'effect'

class MediaListType(Enum):
    Loop = 'Loop'
    Burn = 'Burn'

class MediaItem():
    def __init__(self, path ='', name = '', media_id = '', type = 1, created = '', cover = '', plays = 0 , rank = 1) -> None:
        
        #if a path is not provided, create a blank MediaItem object. 
        if not path:
            return 

        if(media_id):
            self.id = media_id
        else: 
            self.id = (sha1(bytes(str(time()),'UTF-8'))).hexdigest()

        if(created):
            self.created = created
        else: 
            self.created = str(time())

        self.type = MediaItemType(type)   
        self.path = path
        self.filename = self.path.split('/')[-1]
        self.plays = plays
        self.rank = rank
        self.runtime = self.get_runtime(self.path)

        if(name):
            self.name = name
        else: 
            self.name = self.path.split('/')[-1][0:(self.file_name.rindex("."))]

        if(cover):
            self.cover = cover
        else: 
            if exists("Directory the the cover from storage" + self.name):
                self.cover = self.name
            else: 
                if(self.type is MediaItemType.Music):
                    self.cover = 'path to default music icon'
                elif(self.type is MediaItemType.Podcast):
                    self.cover = 'path to default podcast icon'
                elif(self.type is MediaItemType.Weather):
                    self.cover = 'path to default weather icon'
                elif(self.type is MediaItemType.Effect):
                    self.cover = 'path to default effect icon'

    def json_serialise(self, as_string = False) -> dict | str:
        serialised = {
            'id' : self.id,
            'name' : self.name,
            'type' : self.type,
            'path' : self.path,
            'filename' : self.filename,
            'cover' : self.cover,
            'runtime' : self.get_runtime(self.path),
            'plays' : self.plays,
            'rank' : self.rank,
            'created' : self.created
        }
        
        if(as_string):
            serialised = json.dump(serialised)
        
        return serialised

    def deserialise(self, serialised_media) -> None:
        self.id = serialised_media['id']
        self.name = serialised_media['name']
        self.type = serialised_media['type']
        self.path = serialised_media['path']
        self.filename = serialised_media['filename']
        self.cover = serialised_media['cover'] 
        self.plays = serialised_media['plays']
        self.runtime = serialised_media['runtime']
        self.rank = serialised_media['rank']
        self.created = serialised_media['created']

    def get_runtime(self, path):
        print(path)
        #some logic to calculate how long a song might be in seconds. 
        return 100

class MediaList():
    def __init__(self) -> None:
        self.id = ''
        self.name = ''
        self.type = ''
        self.order = ''
        self.items = []
        self.interuptable = []
        self.created = ''

        #asociated with a JSON file. 
        pass

    def __iter__(self):
        self.current_index = 0
        return self
        
    def __next__(self) -> MediaItem | str:
        self.update()
        # return the next item in the media list. 
        if(self.current_index < 1):
            return 'HELLo'
        else:
            if(self.type is MediaListType.Burn):
                raise StopIteration
            self.current_index = 0 

    def insert(self, item: MediaItem) -> None:
        self.items.append(item)

    def remove(self, item: MediaItem) -> None:
        self.items.append(item)

    def update(self, item: str | None) -> None:
        pass

    def json_serialise(self, as_string = False) -> dict | str:
        serialised = {
            'id' : self.id,
            'name' : self.name,
            'type' : self.type,
            'order' : self.order,
            'interuptable' : self.interuptable,
            'items' : self.items,
            'created' : self.created
        }
        
        if(as_string):
            serialised = json.dump(serialised)
        
        return serialised

    def deserialise(self, serialised_list: dict) -> None:
        self.id = serialised_list['id']
        self.name = serialised_list['name']
        self.type = serialised_list['type']
        self.order = serialised_list['order']
        self.interuptable = serialised_list['interuptable']
        self.items = serialised_list['items']
        self.created = serialised_list['created']

class MediaLibrary():
    def __init__(self) -> None:
        self.items: list[MediaItem] = []
        self.lists: list[MediaList] = []
        self.playback_order = "idc"

        with open((path.relpath('storage/library.json')), 'r') as library_json:
            library = json.load(library_json)

        #Put all of the media items into the main library
        for item in library['items']:
            media_item = MediaItem()
            media_item.deserialise(item)
            self.items.append(media_item)
        
        #Generate all the media lists. 
        for media_list in library['lists']:
            media_list = MediaList()
            media_list.deserialise(media_list)
            self.lists.append(media_list)

    def insert(self, item: MediaItem) -> None:
        self.items.append(item)
        pass

    def remove(self, item: MediaItem) -> None:
        self.items.remove(item)
        #remove a given Media
        pass

    def new_list(self, name, media_list: MediaList):
        self.lists.append(media_list)
        #creates new media json files. and media lists we can manage later. 
        pass
    def del_list(self, media_list: MediaList):
        self.lists.append(media_list)
        #creates new media json files. and media lists we can manage later. 
        pass




def get_current_queue() -> dict:
    '''
    A dictionary of the queue the program hanlder is currently reading. 
    @return dict with keys:
    'type': 'loop'|'burn',
    'interuptable': boolean,
    'items': dict[],
    '''
    #load the status.json file that contains infomation like what the current queue that should be playing is. 
    with open((path.relpath('storage/status.json')), 'r') as status:
        current = json.load(status)

    path_to_file = path.relpath('storage/queues/' + current['current_queue'] + '.json')
    #load the correct queue
    with open(path_to_file, 'r') as current_queue:
        current = json.load(current_queue)
        current['path'] = path_to_file

    return current

def update_queue(queue: dict, new_queue:dict) -> None:
    '''
    Helper function to update the queue json file, when  the queue is modified. 
    @param queue
    @param new_queue
    '''
    #overwrite the queue with the new updated que infomation
    with open(queue['path'], 'w') as current_queue:
        json.dump(new_queue, current_queue)

def get_interupt() -> dict:
    '''
    Checks the interupt queue and returns the oldest item in the queue.
    @return media item dictionary.
    'id': str,
    'name': str,
    'cover': str,
    'path': str,
    'plays': int,
    'type': 'music'|'weather'|'podcast'
    '''
    #open the interupts json and return the oldest item in the interupt queue. 

    with open((path.relpath('storage/queues/interupts.json')), 'r') as interupt_queue:
        interupts = json.load(interupt_queue)
        interupts['path'] = 'storage/queues/interupts.json'
      
    if(interupts['items']):
        interupt = interupts['items'][0]
        del interupts['items'][0]
        update_queue(interupts,interupts)
    else:
        interupt = None

    return interupt

def get_next() -> dict:
    '''
    Helper function for get_programme_list that checks the currently playing queue, or other relevant queues to return the next item to serve the program list generator.
    'id': str,
    'name': str,
    'cover': str,
    'path': str,
    'plays': int,
    'type': 'music'|'weather'|'podcast'
    '''
    queue = get_current_queue()

    if(queue['type'] == 'loop'):
        #check for interupts that we could potentially play right now instead.
        next_item = get_interupt()

        if not next_item:
            next_item = queue['items'][-1]
            queue['items'].insert(0,next_item)
            del queue['items'][-1]
            update_queue(queue, queue)

    else:
        if(queue['items']):
            next_item = queue['items'][-1]
            del queue['items'][-1]
            update_queue(queue, queue)
        else:
            next_item = None

    return next_item
      
def get_programme_list():
    '''
    Returns a generator of programmes (items) to play next based on what is current queue prefrences
    @return dict[] generator each elements has keys:
    'id': str,
    'name': str,
    'cover': str,
    'path': str,
    'plays': int,
    'type': 'music'|'weather'|'podcast'
    '''
    while(True):
        item = get_next()
        if(item):
            response = MediaItem(item['path'], 'music')
            yield response
        else:
            yield False

def insert_programme(queue, item):

    pass

def remove_programe(queue, item):
    pass

def load_media(item):
    pass

def injest_media(item: MediaItem):
    library = {}
    with open((path.relpath('storage/library.json')), 'r') as library_json:
        library = json.load(library_json)
    update_queue(library, library['items'].append(item.json_serialise))

def remove_item(item: MediaItem):
    library = {}
    with open((path.relpath('storage/library.json')), 'r') as library_json:
     library = json.load(library_json)
    update_queue(library, library['items'].remove(item.json_serialise))