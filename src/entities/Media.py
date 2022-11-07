import json
from os.path import exists
from enum import Enum
from hashlib import sha1
from time import  time
from tinydb import TinyDB, where
from HMPConfig import *

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

    def __init__(self, path ='', name = '', media_id = None, type = 'music', created =  None, cover = '', plays = 0 , rank = 1) -> None:
        
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
            if exists("Directory the the cover from storage" + self.name + '.png'):
                self.cover = self.name
            else: 
                if(self.type is MediaItemType.Music):
                    self.cover = DEFAULT_COVERS + MediaItemType.Music.value + '.png'
                elif(self.type is MediaItemType.Podcast):
                    self.cover = DEFAULT_COVERS + MediaItemType.Podcast.value  + '.png'
                elif(self.type is MediaItemType.Weather):
                    self.cover = DEFAULT_COVERS + MediaItemType.Weather.value  + '.png'
                elif(self.type is MediaItemType.Effect):
                    self.cover = DEFAULT_COVERS + MediaItemType.Effect.value  + '.png'

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
    
    def update_media_item(self, updated_item: MediaItem) -> None:
        item = self.get_media_item(updated_item.id)
    
        if(item.name != updated_item.name and updated_item.name):
            item.name = updated_item.name
        
        if(item.type != updated_item.type and updated_item.type):
            item.type = updated_item.type

        if(item.cover != updated_item.cover and updated_item.cover):
            item.cover = updated_item.cover

        if(item.plays != updated_item.plays and updated_item.plays):
            item.plays = updated_item.plays
        
        if(item.rank != updated_item.rank and updated_item.rank):
            item.rank = updated_item.rank

        self.remove_media_item(item.id)
        self.insert_media_item(item)
    
    def remove_media_item(self, item: MediaItem | str) -> None:
        if(isinstance(item, MediaItem)):
            item = item.id
        media_item = (list(self.libaray.search(where('id') == item)))[0]
        self.libaray.remove(media_item)

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