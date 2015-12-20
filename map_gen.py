# Note - x0,y0 is the North West
import settings
import color
from place_objects import place_objects
from Object import Object
from Tile import Tile
from Rect import Rect


def make_map(corner=0):
    settings.objects = [settings.player]
    settings.map = [[Tile(True) for y in range(settings.MAP_HEIGHT)]
                    for x in range(settings.MAP_WIDTH)]
    settings.flood_map = [[-1 for y in range(settings.MAP_HEIGHT)]
                          for x in range(settings.MAP_WIDTH)]
    rooms = []
    num_rooms = 1

    if num_rooms == 0 and corner == 0:
        corner = settings.RNG.get_int(0, 3)

    w = settings.RNG.get_int(settings.ROOM_MIN_SIZE,
                             settings.ROOM_MAX_SIZE)
    h = settings.RNG.get_int(settings.ROOM_MIN_SIZE,
                             settings.ROOM_MAX_SIZE)
    if corner == 0:   # North West
        x = settings.RNG.get_int(0, (settings.MAP_WIDTH - w - 1) / 3)
        y = settings.RNG.get_int(0, (settings.MAP_HEIGHT - h - 1) / 3)
    elif corner == 1:   # North East
        x = settings.RNG.get_int(settings.MAP_WIDTH / 3,
                                 settings.MAP_WIDTH - w - 1)
        y = settings.RNG.get_int(0, (settings.MAP_HEIGHT - h - 1) / 3)
    elif corner == 2:   # South West
        x = settings.RNG.get_int(0, (settings.MAP_WIDTH - w - 1) / 3)
        y = settings.RNG.get_int(settings.MAP_HEIGHT / 3,
                                 settings.MAP_HEIGHT - h - 1)
    elif corner == 3:   # South East
        x = settings.RNG.get_int(settings.MAP_WIDTH / 3,
                                 settings.MAP_WIDTH - w - 1)
        y = settings.RNG.get_int(settings.MAP_HEIGHT / 3,
                                 settings.MAP_HEIGHT - h - 1)

    new_room = Rect(x, y, w, h)
    create_room(new_room)
    (settings.player.x, settings.player.y) = new_room.center
    rooms.append(new_room)

    finished = False
    backtrack = 1
    failure_to_place = 0
    while not finished:
        direction = settings.RNG.get_int(1, 4)
        w = settings.RNG.get_int(settings.ROOM_MIN_SIZE,
                                 settings.ROOM_MAX_SIZE)
        h = settings.RNG.get_int(settings.ROOM_MIN_SIZE,
                                 settings.ROOM_MAX_SIZE)
        new_room = Rect(0, 0, w, h)
        (prev_x, prev_y) = rooms[num_rooms - backtrack].center
        distance_varience = settings.RNG.get_int(0, 3)
        wiggle = settings.RNG.get_int(0, w + h) - (w + h) / 2
        if direction == 1:   # North
            new_room.move_by_center(prev_x - wiggle,
                                    prev_y - h - distance_varience)
        elif direction == 2:   # East
            new_room.move_by_center(prev_x + w + distance_varience,
                                    prev_y - wiggle)
        elif direction == 3:   # South
            new_room.move_by_center(prev_x - wiggle,
                                    prev_y + h + distance_varience)
        elif direction == 4:   # West
            new_room.move_by_center(prev_x - w - distance_varience,
                                    prev_y - wiggle)

        (new_x, new_y) = new_room.center
        intersects = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                intersects = True

        if new_room.x1 < 1 or new_room.x2 > settings.MAP_WIDTH - 2 or \
                new_room.y1 < 1 or new_room.y2 > settings.MAP_HEIGHT - 2:
            intersects = True

        if not intersects:
            create_room(new_room)
            place_objects(new_room)
            if settings.RNG.get_int(0, 1):
                create_h_tunnel(prev_x, new_x, prev_y)
                create_v_tunnel(prev_y, new_y, new_x)
            else:
                create_v_tunnel(prev_y, new_y, prev_x)
                create_h_tunnel(prev_x, new_x, new_y)

            rooms.append(new_room)
            num_rooms += 1
            backtrack = 1
            if num_rooms >= settings.MAX_ROOMS:
                finished = True
        else:
            if failure_to_place < 10:
                failure_to_place += 1
            else:
                failure_to_place = 0
                backtrack += 1
                if backtrack > num_rooms:
                    finished = True

    (cx, cy) = get_farthest_floor(settings.player.x, settings.player.y)
    stairs_rect = Rect(cx, cy, 1, 1)
    for other_room in rooms:
        if stairs_rect.intersect(other_room):
            (cx, cy) = other_room.center
    settings.stairs = Object(cx, cy, '<', 'stairs',
                             color.white, always_visible=True)
    settings.objects.append(settings.stairs)
    settings.stairs.send_to_back()


def create_room(room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            settings.map[x][y].blocked = False
            settings.map[x][y].block_sight = False
            settings.flood_map[x][y] = 0


def create_h_tunnel(x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        settings.map[x][y].blocked = False
        settings.map[x][y].block_sight = False
        settings.flood_map[x][y] = 0


def create_v_tunnel(y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        settings.map[x][y].blocked = False
        settings.map[x][y].block_sight = False
        settings.flood_map[x][y] = 0


def get_farthest_floor(px, py):
    filling = True
    far_x = px
    far_y = py
    settings.flood_map[px][py] = 1
    while filling:
        filling = False
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                if settings.flood_map[x][y] == 1:
                    if settings.flood_map[x+1][y] == 0:
                        settings.flood_map[x+1][y] = 1
                        filling = True
                        far_x = x + 1
                        far_y = y
                    elif settings.flood_map[x-1][y] == 0:
                        settings.flood_map[x-1][y] = 1
                        filling = True
                        far_x = x - 1
                        far_y = y
                    elif settings.flood_map[x][y+1] == 0:
                        settings.flood_map[x][y+1] = 1
                        filling = True
                        far_x = x
                        far_y = y + 1
                    elif settings.flood_map[x][y-1] == 0:
                        settings.flood_map[x][y-1] = 1
                        filling = True
                        far_x = x
                        far_y = y - 1

    return(far_x, far_y)
