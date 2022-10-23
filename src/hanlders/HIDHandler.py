from entities.Player import Player

def get_change():
    #Listens to the webpage and listens to physical hardware to no how to change the volume. 
    #Periodicly poll both locations to know how much or a change, or plug directly into the hardware that handles it. 
    return 0

def level_controler(player: Player, data_lock):
    while(True):
                    
        levels_change = get_change()
        if(levels_change < 0):
            player.volume_decrease()
        elif(levels_change > 0):
            player.volume_increase()

        print("looped!" + str(player.name) + "This is thread 1")