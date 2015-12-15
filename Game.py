import shelve
import settings


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

    player_action = None

    mouse = libtcod.Mouse()
    key = libtcod.Key()
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS |
                                    libtcod.EVENT_MOUSE,
                                    key, mouse)
        render_all()

        libtcod.console_flush()

        check_level_up()

        for object in objects:
            object.clear()

        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break

        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for object in objects:
                if object.ai:
                    object.ai.take_turn()


def load_game():
    global map, objects, player, stairs, inventory, game_msgs, \
        game_state, dungeon_level

    file = shelve.open('savegame.save', 'r')
    map = file['map']
    objects = file['objects']
    player = objects[file['player_index']]
    inventory = file['inventory']
    game_msgs = file['game_msgs']
    game_state = file['game_state']
    stairs = objects[file['stairs_index']]
    dungeon_level = file['dungeon_level']
    file.close()

    initialize_fov()


def save_game():
    file = shelve.open('savegame.save', 'n')
    file['map'] = map
    file['objects'] = objects
    file['player_index'] = objects.index(player)
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file['stairs_index'] = objects.index(stairs)
    file['dungeon_level'] = dungeon_level
    file.close()
