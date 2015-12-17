import settings
import shelve


def save_game():
    file = shelve.open('savegame.save', 'n')
    file['map'] = settings.map
    file['objects'] = settings.objects
    file['player_index'] = settings.objects.index(settings.player)
    file['inventory'] = settings.inventory
    file['game_msgs'] = settings.game_msgs
    file['game_state'] = settings.game_state
    file['stairs_index'] = settings.objects.index(settings.stairs)
    file['dungeon_level'] = settings.dungeon_level
    file.close()
