import libtcodpy as libtcod
import shelve
import settings
from Object import Object
from Fighter import Fighter
from Fighter import player_death
from Map import make_map
from message import message
from Equipment import Equipment


def new_game():
    global player, inventory, game_msgs, game_state, dungeon_level

    fighter_component = Fighter(hp=30, defense=2, power=5,
                                xp=0, death_function=player_death)
    player = Object(0, 0, '@', 'player', libtcod.white, blocks=True,
                    fighter=fighter_component)

    player.level = 1
    dungeon_level = 1
    make_map()
    initialize_fov()

    game_state = 'playing'
    inventory = []

    game_msgs = []

    message('Welcome stranger. Prepare to perish in the ' +
            'Tombs of the Ancient Kings.', libtcod.red)

    equipment_component = Equipment(slot='right hand', power_bonus=2)
    obj = Object(0, 0, '-', 'dagger', libtcod.sky,
                 equipment=equipment_component)
    inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True


def play_game():
    global key, mouse, objects, game_state, player_action

    settings.player_action = None

    settings.mouse = libtcod.Mouse()
    settings.key = libtcod.Key()
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS |
                                    libtcod.EVENT_MOUSE,
                                    settings.key, settings.mouse)
        render_all()

        libtcod.console_flush()

        check_level_up()

        for object in settings.objects:
            object.clear()

        settings.player_action = handle_keys()
        if settings.player_action == 'exit':
            save_game()
            break

        if settings.game_state == 'playing' and \
           settings.player_action != 'didnt-take-turn':
            for object in settings.objects:
                if object.ai:
                    object.ai.take_turn()


def load_game():
    file = shelve.open('savegame.save', 'r')
    settings.map = file['map']
    settings.objects = file['objects']
    settings.player = objects[file['player_index']]
    settings.inventory = file['inventory']
    settings.game_msgs = file['game_msgs']
    settings.game_state = file['game_state']
    settings.stairs = objects[file['stairs_index']]
    settings.dungeon_level = file['dungeon_level']
    file.close()

    initialize_fov()


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


def next_level():
    message('You take a moment to rest, and recover your strength',
            libtcod.light_violet)
    player.fighter.heal(player.fighter.max_hp / 2)

    settings.dungeon_level += 1
    message('After a rare moment of peace, you descend deeper into ' +
            'the heart of the dungeon...', libtcod.red)
    make_map()
    initialize_fov()


def initialize_fov():
    settings.fov_recompute = True

    settings.fov_map = libtcod.map_new(settings.MAP_WIDTH, settings.MAP_HEIGHT)
    for y in range(settings.MAP_HEIGHT):
        for x in range(settings.MAP_WIDTH):
            libtcod.map_set_properties(settings.fov_map, x, y,
                                       not settings.map[x][y].block_sight,
                                       not settings.map[x][y].blocked)

    libtcod.console_clear(settings.con)
