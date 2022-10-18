
import json
from os import path
from os.path import exists
import json
from enum import Enum
from hashlib import sha1
from time import sleep, time
from tinydb import TinyDB, Query, where

class MediaItemType(Enum):
    Music = 'music'
    Podcast = 'podcast'
    Weather = 'weather'
    Effect = 'effect'

class MediaListType(Enum):
    Loop = 'loop'
    Burn = 'burn'

class MediaListOrder(Enum):
    Sequential = 'Sequential'
    Reverse = 'reverse'
    Random = 'randmon'
    Shuffle = 'shuffle'

class MediaItem():

    def __init__(self, path ='', name = '', media_id = '', type = 'music', created = '', cover = '', plays = 0 , rank = 1) -> None:
        
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

    def serialise(self, as_string = False) -> dict | str:
        serialised = {
            'id' : self.id,
            'name' : self.name,
            'type' : self.type.value,
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
        #print(path)
        #some logic to calculate how long a song might be in seconds. 
        return 100

class MediaList():
    def __init__(self, name: str, list_id = '', type = 'loop', order = 'sequence', items = [], interuptable = False, created = '') -> None:
        
        if not name:
            return 

        if(list_id):
            self.id = list_id
        else: 
            self.id = (sha1(bytes(str(time()),'UTF-8'))).hexdigest()
        
        self.name = name
        self.type = MediaListType(type)   

        self.order = order

        self.items: list = items
        self.interuptable = interuptable

        if(created):
            self.created = created
        else: 
            self.created = str(time())

    def __iter__(self):
        self.current_index = 0
        return self
        
    def __next__(self) -> str:
        if(self.interuptable):
            interrupt = '1'
            #some how check for interupts from the Media Library
            if(interrupt):
                return interrupt
        

        if(self.current_index < len(self.items)):
            media_item = self.items[self.current_index]
            #if the media list is a burnable list, remove the item from the media list after we have served it. 
            if(self.type is MediaListType.Burn):
                self.items.pop(self.current_index)

            self.current_index+= 1
            #return media_item
        else:
            if(self.type is MediaListType.Loop):
                self.current_index = 0
                media_item = self.items[self.current_index]
                self.current_index+= 1
                #return media_item                
            raise StopIteration
        
        return (MediaLibrary()).get_media_item(media_item)

    def insert(self, item: MediaItem) -> None:
        self.items.append(item.id)

    def remove(self, item: MediaItem) -> None:
        self.items.append(item)

    def update(self, item: str | None) -> None:
        pass

    def serialise(self, as_string = False) -> dict | str:
        serialised = {
            'id' : self.id,
            'name' : self.name,
            'type' : self.type.value,
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
    '''
    This is a singleton of all the media we have in the media libaray, there will only ever one instance of this object. 

    '''
    __instance = None

    def __new__(cls):
        if(cls.__instance is None):
            cls.__instance = super(MediaLibrary, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.libaray = TinyDB('library.json')
        self.lists = TinyDB('media_lists.json')

    def get_media_item(self, object_id: str) -> MediaItem:

        media_item = (list(self.libaray.search(where('id') == object_id)))[0]
        return MediaItem(
            media_item['path'],
            media_item['name'],
            media_item['id'],
            media_item['type'],
            media_item['created'],
            media_item['cover'],
            media_item['rank'],
            media_item['plays'])
        
    def insert_media_item(self, item: MediaItem) -> None:
        self.libaray.insert(item.serialise())
    
    def update_media_item(self, item: MediaItem) -> None:
        self.libaray.update()
    
    def remove_media_item(self, item: MediaItem) -> None:
        self.libaray.remove()

    def get_media_list(self, object_id: str) -> MediaList:
        media_list = (list(self.lists.search(where('id') == object_id)))[0]
        return MediaList(
            media_list['name'],
            media_list['id'],
            media_list['type'],
            media_list['order'],
            media_list['items'],
            media_list['interuptable'],
            media_list['created'])

    def insert_media_list(self, name, media_list: MediaList):
        self.lists.insert()

    def update_media_list(self, name, media_list: MediaList, ):
        self.lists.update()

    def remove_media_list(self, media_list: MediaList) -> None:
        self.lists.remove()


# library = MediaLibrary()

# thing = library.get_media_list('123edasd21VA')
# for thing in library.get_media_list('123edasd21VA'):
#     print(library.get_media_item(thing).type)

    
#print(list(library.lists.all()))
        # {
        #     "id": 1,
        #     "name": "MV Jack Stauber - Buttercup",
        #     "cover": "",
        #     "path": "storage/media/MV Jack Stauber - Buttercup.mp3",
        #     "plays": 0,
        #     "type": "music"
        # },









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



def start(): 

    pass