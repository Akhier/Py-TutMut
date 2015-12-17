import libtcodpy as libtcod
import settings
from message import message


def cast_heal():
    if settings.player.fighter.hp == settings.player.fighter.max_hp:
        message('You are already at full health.', libtcod.red)
        return 'cancel'

    message('Your wounds start to feel better.', libtcod.light_violet)
    settings.player.fighter.heal(settings.HEAL_AMOUNT)


def cast_lightning():
    monster = closest_monster(settings.LIGHTNING_RANGE)
    if monster is None:
        message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'

    message('A lightning bolt strikes the ' + monster.name +
            ' with a loud thunder! the damage is ' +
            str(settings.LIGHTNING_DAMAGE) + ' hit points.',
            libtcod.light_blue)
    monster.fighter.take_damage(settings.LIGHTNING_DAMAGE)


def cast_fireball():
    message('Left-click a target tile for the fireball,' +
            ' or right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()
    if x is None:
        return 'cancelled'
    message('The fireball explodes, burning everything within ' +
            str(settings.FIREBALL_RADIUS) + ' tiles.', libtcod.orange)

    for obj in settings.objects:
        if obj.distance(x, y) <= settings.FIREBALL_RADIUS and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' +
                    str(settings.FIREBALL_DAMAGE) +
                    ' hit points.', libtcod.orange)
            obj.fighter.take_damage(settings.FIREBALL_DAMAGE)


def cast_confuse():
    from AI import ConfusedMonster
    monster = closest_monster(settings.CONFUSE_RANGE)
    message('Left-click an enemy to confuse it, or right-click to cancel.',
            libtcod.light_cyan)
    monster = target_monster(settings.CONFUSE_RANGE)
    if monster is None:
        return 'cancelled'

    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster
    message('The eyes of the ' + monster.name +
            ' look vacant, as he starts to stumble around.',
            libtcod.light_green)


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
