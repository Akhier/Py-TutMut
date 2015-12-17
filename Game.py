import libtcodpy as libtcod
import shelve
import settings
from Object import Object
from Fighter import Fighter
from Map import make_map
from message import message
from Equipment import Equipment
from render_all import render_all
from Menu import menu
from handle_keys import handle_keys
from handle_keys import initialize_fov


def new_game():
    fighter_component = Fighter(hp=30, defense=2, power=5,
                                xp=0, death_function=player_death)
    settings.player = Object(0, 0, '@', 'player', libtcod.white, blocks=True,
                             fighter=fighter_component)

    settings.player.level = 1
    settings.dungeon_level = 1
    make_map()
    initialize_fov()

    settings.game_state = 'playing'
    settings.inventory = []

    settings.game_msgs = []

    message('Welcome stranger. Prepare to perish in the ' +
            'Tombs of the Ancient Kings.', libtcod.red)

    equipment_component = Equipment(slot='right hand', power_bonus=2)
    obj = Object(0, 0, '-', 'dagger', libtcod.sky,
                 equipment=equipment_component)
    settings.inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True


def play_game():
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
    settings.player = settings.objects[file['player_index']]
    settings.inventory = file['inventory']
    settings.game_msgs = file['game_msgs']
    settings.game_state = file['game_state']
    settings.stairs = settings.objects[file['stairs_index']]
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


def check_level_up():
    level_up_xp = settings.LEVEL_UP_BASE + settings.player.level * \
        settings.LEVEL_UP_FACTOR
    if settings.player.fighter.xp >= level_up_xp:
        settings.player.level += 1
        settings.player.fighter.xp -= level_up_xp
        message('Your battle skills grow stronger. You reached level ' +
                str(settings.player.level) + '.', libtcod.yellow)

        choice = None
        while choice is None:
            choice = menu('Level up! Choose a stat to raise:\n',
                          ['Constitution (+20 HP, from ' +
                           str(settings.player.fighter.max_hp) + ')',
                           'Strength (+1 attack, from ' +
                           str(settings.player.fighter.power) + ')',
                           'Agility (+1 defense, from ' +
                           str(settings.player.fighter.defense) + ')'],
                          settings.LEVEL_SCREEN_WIDTH)

        if choice == 0:
            settings.player.fighter.max_hp += 20
            settings.player.fighter.hp += 20
        elif choice == 1:
            settings.player.fighter.power += 1
        elif choice == 2:
            settings.player.fighter.defense += 1


def player_death(player):
    global game_state
    print('you died.')
    game_state = 'dead'

    settings.player.char = '%'
    settings.player.color = libtcod.dark_red
