import json
from os import path

#multiple queues? 

#you make a queue which is a list of music, and songs, and depending on data about the queue, such as if the queue is set to repeat
#either end the queue or return to the last time of the queue with each play.
#We don't realisticly care what the real time order of the queue is so we can continue from where ever the queue left off when we resume. 

#we can also interget events like time so particular queues always play at particular moments in time. 


def get_current_queue() -> dict:
    #load the status.json file that contains infomation like what the current queue that should be playing is. 
    with open((path.relpath("storage/status.json")), 'r') as status:
        current = json.load(status)

    path_to_file = path.relpath("storage/queues/" + current["current_queue"] + ".json")
    #load the correct queue
    with open(path_to_file, 'r') as current_queue:
        current = json.load(current_queue)
        current["path"] = path_to_file

    return current

def update_queue(queue, new_queue):
    #overwrite the queue with the new updated que infomation
    with open(queue["path"], "w") as current_queue:
        json.dump(new_queue, current_queue)

def get_interupt():
    pass

def get_next():
    queue = get_current_queue()

    if(queue["type"] == "loop"):
        #check for interupts that we could potentially play right now instead.
        next_item = get_interupt()

        if not next_item:
            next_item = queue["items"][-1]
            queue["items"].insert(0,next_item)
            del queue["items"][-1]
            update_queue((get_current_queue), queue)

    else:
        next_item = queue["items"][-1]
        del queue["items"][-1]
        update_queue((get_current_queue), queue)

    return next_item
      
def get_programme_list():
    while(True):
        item = get_next()
        if(item):
            yield item
        else:
            break
    return None

print(get_current_queue())
