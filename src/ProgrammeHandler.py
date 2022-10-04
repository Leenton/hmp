import json
from os import path

def get_current_queue() -> dict:
    '''
    A dictionary of the queue the program hanlder is currently reading. 
    @return dict with keys:
    'type': 'loop'|'burn',
    'interuptable': boolean,
    'items': dict[],
    '''
    #load the status.json file that contains infomation like what the current queue that should be playing is. 
    with open((path.relpath("storage/status.json")), 'r') as status:
        current = json.load(status)

    path_to_file = path.relpath("storage/queues/" + current["current_queue"] + ".json")
    #load the correct queue
    with open(path_to_file, 'r') as current_queue:
        current = json.load(current_queue)
        current["path"] = path_to_file

    return current

def update_queue(queue: dict, new_queue:dict) -> None:
    '''
    Helper function to update the queue json file, when  the queue is modified. 
    @param queue
    @param new_queue
    '''
    #overwrite the queue with the new updated que infomation
    with open(queue["path"], "w") as current_queue:
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

    with open((path.relpath("storage/queues/interupts.json")), 'r') as interupt_queue:
        interupts = json.load(interupt_queue)
        interupts["path"] = "storage/queues/interupts.json"
      
    if(interupts["items"]):
        interupt = interupts["items"][0]
        del interupts["items"][0]
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

    if(queue["type"] == "loop"):
        #check for interupts that we could potentially play right now instead.
        next_item = get_interupt()

        if not next_item:
            next_item = queue["items"][-1]
            queue["items"].insert(0,next_item)
            del queue["items"][-1]
            update_queue(queue, queue)

    else:
        if(queue["items"]):
            next_item = queue["items"][-1]
            del queue["items"][-1]
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
            yield item
        else:
            break
    return None

def insert_programme(queue, item):
    pass