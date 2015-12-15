import libtcodpy as libtcod
import settings
import Item
from Tile import Tile
from Rect import Rect
from Object import Object
from Object import is_blocked
from Fighter import Fighter
from Fighter import monster_death
from Equipment import Equipment
from AI import BasicMonster


def make_map():
    settings.objects = [settings.player]

    settings.map = [[Tile(True) for y in range(settings.MAP_HEIGHT)]
                    for x in range(settings.MAP_WIDTH)]

    rooms = []
    num_rooms = 0

    for r in range(settings.MAX_ROOMS):
        w = libtcod.random_get_int(0, settings.ROOM_MIN_SIZE,
                                   settings.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, settings.ROOM_MIN_SIZE,
                                   settings.ROOM_MAX_SIZE)
        x = libtcod.random_get_int(0, 0, settings.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, settings.MAP_HEIGHT - h - 1)

        new_room = Rect(x, y, w, h)

        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            create_room(new_room)
            place_objects(new_room)
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                settings.player.x = new_x
                settings.player.y = new_y
            else:
                (prev_x, prev_y) = rooms[num_rooms - 1].center()
                if libtcod.random_get_int(0, 0, 1) == 1:
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            rooms.append(new_room)
            num_rooms += 1

    settings.stairs = Object(new_x, new_y, '<', 'stairs',
                             libtcod.white, always_visible=True)
    settings.objects.append(settings.stairs)
    settings.stairs.send_to_back()


def create_room(room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            settings.map[x][y].blocked = False
            settings.map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        settings.map[x][y].blocked = False
        settings.map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        settings.map[x][y].blocked = False
        settings.map[x][y].block_sight = False


def place_objects(room):
    max_monster = from_dungeon_level([[2, 1], [3, 4], [5, 6]])

    monster_chances = {}
    monster_chances['orc'] = 80
    monster_chances['troll'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])

    max_items = from_dungeon_level([[1, 1], [2, 4]])

    item_chances = {}
    item_chances['heal'] = 35
    item_chances['lightning'] = from_dungeon_level([[25, 4]])
    item_chances['fireball'] = from_dungeon_level([[25, 6]])
    item_chances['confuse'] = from_dungeon_level([[10, 2]])
    item_chances['sword'] = from_dungeon_level([[5, 4]])
    item_chances['shield'] = from_dungeon_level([[15, 8]])

    num_monsters = libtcod.random_get_int(0, 0, max_monster)

    for i in range(num_monsters):
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        if not is_blocked(x, y):
            choice = random_choice(monster_chances)
            if choice == 'orc':
                fighter_component = Fighter(hp=10, defense=0, power=3, xp=35,
                                            death_function=monster_death)
                ai_component = BasicMonster()

                monster = Object(x, y, 'o', 'orc', libtcod.desaturated_green,
                                 blocks=True, fighter=fighter_component,
                                 ai=ai_component)
            elif choice == 'troll':
                fighter_component = Fighter(hp=16, defense=1, power=4, xp=100,
                                            death_function=monster_death)
                ai_component = BasicMonster()

                monster = Object(x, y, 'T', 'troll', libtcod.darker_green,
                                 blocks=True, fighter=fighter_component,
                                 ai=ai_component)

            settings.objects.append(monster)

    num_items = libtcod.random_get_int(0, 0, max_items)

    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        if not is_blocked(x, y):
            choice = random_choice(item_chances)
            if choice == 'heal':
                item_component = Item.Item(use_function=Item.cast_heal)
                item = Object(x, y, '!', 'healing potion',
                              libtcod.violet, item=item_component)
            elif choice == 'lightning':
                item_component = Item.Item(use_function=Item.cast_lightning)
                item = Object(x, y, '#', 'scroll of lightning bolt',
                              libtcod.light_yellow, item=item_component)
            elif choice == 'fireball':
                item_component = Item.Item(use_function=Item.cast_fireball)
                item = Object(x, y, '#', 'scroll of fireball',
                              libtcod.light_yellow, item=item_component)
            elif choice == 'confuse':
                item_component = Item.Item(use_function=Item.cast_confuse)
                item = Object(x, y, '#', 'scroll of confusion',
                              libtcod.light_yellow, item=item_component)
            elif choice == 'sword':
                equipment_component = Equipment(slot='right hand',
                                                power_bonus=3)
                item = Object(x, y, '/', 'sword', libtcod.sky,
                              equipment=equipment_component)
            elif choice == 'shield':
                equipment_component = Equipment(slot='right hand',
                                                defense_bonus=1)
                item = Object(x, y, '[', 'shield', libtcod.darker_orange,
                              equipment=equipment_component)
            settings.objects.append(item)
            item.send_to_back()
            item.always_visible = True


def from_dungeon_level(table):
    for (value, level) in reversed(table):
        if settings.dungeon_level >= level:
            return value
    return 0


def random_choice(chances_dict):
    chances = chances_dict.values()
    strings = chances_dict.keys()

    return strings[random_choice_index(chances)]


def random_choice_index(chances):
    dice = libtcod.random_get_int(0, 1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if dice <= running_sum:
            return choice
        choice += 1
