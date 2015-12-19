import targeting
import settings
import color
from message import message


def cast_heal():
    if settings.player.fighter.hp == settings.player.fighter.max_hp:
        message('You are already at full health.', color.red)
        return 'cancel'

    message('Your wounds start to feel better.', color.light_violet)
    settings.player.fighter.heal(settings.HEAL_AMOUNT)


def cast_lightning():
    monster = targeting.closest_monster(settings.LIGHTNING_RANGE)
    if monster is None:
        message('No enemy is close enough to strike.', color.red)
        return 'cancelled'

    message('A lightning bolt strikes the ' + monster.name +
            ' with a loud thunder! the damage is ' +
            str(settings.LIGHTNING_DAMAGE) + ' hit points.',
            color.light_blue)
    monster.fighter.take_damage(settings.LIGHTNING_DAMAGE)


def cast_fireball():
    message('Left-click a target tile for the fireball,' +
            ' or right-click to cancel.', color.light_cyan)
    (x, y) = targeting.target_tile()
    if x is None:
        return 'cancelled'
    message('The fireball explodes, burning everything within ' +
            str(settings.FIREBALL_RADIUS) + ' tiles.', color.orange)

    for obj in settings.objects:
        if obj.distance(x, y) <= settings.FIREBALL_RADIUS and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' +
                    str(settings.FIREBALL_DAMAGE) +
                    ' hit points.', color.orange)
            obj.fighter.take_damage(settings.FIREBALL_DAMAGE)


def cast_confuse():
    from AI import ConfusedMonster
    monster = targeting.closest_monster(settings.CONFUSE_RANGE)
    message('Left-click an enemy to confuse it, or right-click to cancel.',
            color.light_cyan)
    monster = targeting.target_monster(settings.CONFUSE_RANGE)
    if monster is None:
        return 'cancelled'

    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster
    message('The eyes of the ' + monster.name +
            ' look vacant, as he starts to stumble around.',
            color.light_green)
