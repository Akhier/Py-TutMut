import libtcodpy as libtcod
import settings


def closest_monster(max_range):
    closest_enemy = None
    closest_dist = max_range + 1

    for object in settings.objects:
        if object.fighter and not object == settings.player and \
           libtcod.map_is_in_fov(settings.fov_map, object.x, object.y):
            dist = settings.player.distance_to(object)
            if dist < closest_dist:
                closest_enemy = object
                closest_dist = dist
    return closest_enemy


def target_monster(max_range=None):
    while True:
        (x, y) = target_tile(max_range)
        if x is None:
            return None

        for obj in settings.objects:
            if obj.x == x and obj.y == y and \
                    obj.fighter and obj != settings.player:
                return obj


def target_tile(max_range=None):
    from render_all import render_all
    while True:
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS |
                                    libtcod.EVENT_MOUSE, settings.key,
                                    settings.mouse)
        render_all()

        (x, y) = (settings.mouse.cx, settings.mouse.cy)

        if settings.mouse.rbutton_pressed or \
           settings.key.vk == libtcod.KEY_ESCAPE:
            return (None, None)

        if (settings.mouse.lbutton_pressed and
            libtcod.map_is_in_fov(settings.fov_map, x, y) and
            (max_range is None or
             settings.player.distance(x, y) <= max_range)):
            return (x, y)
