import libtcodpy as libtcod
import settings
import color
from map_gen import make_map
from message import message
from Rect import Rect
from menu import menu


def handle_keys():
    if settings.key.vk == libtcod.KEY_ENTER and settings.key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif settings.key.vk == libtcod.KEY_ESCAPE:
        return 'exit'

    if settings.game_state == 'playing':
        if settings.key.vk == libtcod.KEY_UP or \
                settings.key.vk == libtcod.KEY_KP8:
            player_move_or_attack(0, -1)
        elif settings.key.vk == libtcod.KEY_DOWN or \
                settings.key.vk == libtcod.KEY_KP2:
            player_move_or_attack(0, 1)
        elif settings.key.vk == libtcod.KEY_LEFT or \
                settings.key.vk == libtcod.KEY_KP4:
            player_move_or_attack(-1, 0)
        elif settings.key.vk == libtcod.KEY_RIGHT or \
                settings.key.vk == libtcod.KEY_KP6:
            player_move_or_attack(1, 0)
        elif settings.key.vk == libtcod.KEY_HOME or \
                settings.key.vk == libtcod.KEY_KP7:
            player_move_or_attack(-1, -1)
        elif settings.key.vk == libtcod.KEY_PAGEUP or \
                settings.key.vk == libtcod.KEY_KP9:
            player_move_or_attack(1, -1)
        elif settings.key.vk == libtcod.KEY_END or \
                settings.key.vk == libtcod.KEY_KP1:
            player_move_or_attack(-1, 1)
        elif settings.key.vk == libtcod.KEY_PAGEDOWN or \
                settings.key.vk == libtcod.KEY_KP3:
            player_move_or_attack(1, 1)
        elif settings.key.vk == libtcod.KEY_KP5:
            pass

        else:
            key_char = chr(settings.key.c)

            if key_char == 'g':
                for object in settings.objects:
                    if object.x == settings.player.x and \
                       object.y == settings.player.y and object.item:
                        object.item.pick_up()
                        break

            if key_char == 'i':
                chosen_item = inventory_menu('Press the key next to an ' +
                                             'item to use it, or any ' +
                                             'other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()

            if key_char == 'd':
                chosen_item = inventory_menu('Press the key next to an ' +
                                             'to drop it, or any ' +
                                             'other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()

            if key_char == 'c':
                level_up_xp = settings.LEVEL_UP_BASE + \
                    settings.player.level * \
                    settings.LEVEL_UP_FACTOR
                msgbox('Character information\n\nLevel: ' +
                       str(settings.player.level) +
                       '\nExperiance: ' + str(settings.player.fighter.xp) +
                       '\nExperiance to level up: ' + str(level_up_xp) +
                       '\nMaximum HP: ' + str(settings.player.fighter.max_hp) +
                       '\nAttack: ' + str(settings.player.fighter.power) +
                       '\nDefense: ' + str(settings.player.fighter.defense),
                       settings.CHARACTER_SCREEN_WIDTH)

            if key_char == '<':
                if settings.stairs.x == settings.player.x and \
                        settings.stairs.y == settings.player.y:
                    next_level()

            return 'didnt-take-turn'


def next_level():
    message('You take a moment to rest, and recover your strength',
            color.light_violet)
    settings.player.fighter.heal(settings.player.fighter.max_hp / 2)

    settings.dungeon_level += 1
    message('After a rare moment of peace, you descend deeper into ' +
            'the heart of the dungeon...', color.red)
    (cx, cy) = Rect(0, 0, settings.MAP_WIDTH, settings.MAP_HEIGHT).center
    if settings.stairs.x < cx:
        cx = 0
    else:
        cx = 1
    if settings.stairs.y < cy:
        cy = 0
    else:
        cy = 2
    make_map(cx + cy)
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


def player_move_or_attack(dx, dy):
    x = settings.player.x + dx
    y = settings.player.y + dy

    target = None
    for object in settings.objects:
        if object.fighter and object.x == x and object.y == y:
            target = object
            break

    if target is not None:
        settings.player.fighter.attack(target)
    else:
        settings.player.move(dx, dy)
        settings.fov_recompute = True


def msgbox(text, width=50):
    menu(text, [], width)


def inventory_menu(header):
    if len(settings.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in settings.inventory:
            text = item.name
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)

    index = menu(header, options, settings.INVENTORY_WIDTH)

    if index is None or len(settings.inventory) == 0:
        return None
    return settings.inventory[index].item
