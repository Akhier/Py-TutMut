import libtcodpy as libtcod
import settings
from message import message


class Item:

    global inventory, objects, player

    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        if len(inventory) >= 26:
            message('Your inventory is full, you cannot pick up ' +
                    self.owner.name + '.', libtcod.red)
        else:
            inventory.append(self.owner)
            objects.remove(self.owner)
            message('You picked up a ' + self.owner.name + '.', libtcod.green)

            equipment = self.owner.equipment
            if equipment and get_equipped_in_slot(equipment.slot) is None:
                equipment.equip()

    def drop(self):
        if self.owner.equipment:
            self.owner.equipment.dequip()

        objects.append(self.owner)
        inventory.remove(self.owner)
        self.owner.x = player.x
        self.owner.y = player.y
        message('You dropped a ' + self.owner.name + '.', libtcod.yellow)

    def use(self):
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner)


def cast_heal():
    if player.fighter.hp == player.fighter.max_hp:
        message('You are already at full health.', libtcod.red)
        return 'cancel'

    message('Your wounds start to feel better.', libtcod.light_violet)
    player.fighter.heal(settings.HEAL_AMOUNT)


def cast_lightning():
    monster = closest_monster(settings.LIGHTNING_RANGE)
    if monster is None:
        message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'

    message('A lightning bolt strikes the ' + monster.name +
            ' with a loud thunder! the damage is ' +
            str(LIGHTNING_DAMAGE) + ' hit points.',
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

    for obj in objects:
        if obj.distance(x, y) <= settings.FIREBALL_RADIUS and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' +
                    str(settings.FIREBALL_DAMAGE) +
                    ' hit points.', libtcod.orange)
            obj.fighter.take_damage(settings.FIREBALL_DAMAGE)


def cast_confuse():
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
    global fov_map, player, objects
    closest_enemy = None
    closest_dist = max_range + 1

    for object in objects:
        if object.fighter and not object == player and \
           libtcod.map_is_in_fov(fov_map, object.x, object.y):
            dist = player.distance_to(object)
            if dist < closest_dist:
                closest_enemy = object
                closest_dist = dist
    return closest_enemy
