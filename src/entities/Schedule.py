class schedule():
    '''
    This is a singleton of all the media we have in the media libaray, there will only ever one instance of this object. 

    '''
    __instance = None

    def __new__(cls):
        if(cls.__instance is None):
            cls.__instance = super(schedule, cls).__new__(cls)
        return cls.__instance

