import libtcodpy as libtcod
import settings
from place_objects import place_objects
from Object import Object
from Tile import Tile
from Rect import Rect


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
