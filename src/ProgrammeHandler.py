def get_next():
    #decide the next item to play from the feed or database. 
    return "HELLO"
    
    

def get_programme_list():
    while(True):
        item = get_next()
        if(item):
            yield item
        else:
            break
    return None