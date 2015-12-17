import handle_keys
import settings
import shelve


def load_game():
    file = shelve.open('savegame.save', 'r')
    settings.map = file['map']
    settings.objects = file['objects']
    settings.player = settings.objects[file['player_index']]
    settings.inventory = file['inventory']
    settings.game_msgs = file['game_msgs']
    settings.game_state = file['game_state']
    settings.stairs = settings.objects[file['stairs_index']]
    settings.dungeon_level = file['dungeon_level']
    file.close()
    handle_keys.initialize_fov()
