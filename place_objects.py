import libtcodpy as libtcod
import settings
import Object
import spells
import color
from Equipment import Equipment
from Fighter import Fighter
from message import message
from AI import BasicMonster
from Item import Item


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

        if not Object.is_blocked(x, y):
            choice = random_choice(monster_chances)
            if choice == 'orc':
                fighter_component = Fighter(hp=10, defense=0, power=3, xp=35,
                                            death_function=monster_death)
                ai_component = BasicMonster()

                monster = Object.Object(x, y, 'o', 'orc',
                                        color.desaturated_green,
                                        blocks=True, fighter=fighter_component,
                                        ai=ai_component)
            elif choice == 'troll':
                fighter_component = Fighter(hp=16, defense=1, power=4, xp=100,
                                            death_function=monster_death)
                ai_component = BasicMonster()

                monster = Object.Object(x, y, 'T', 'troll',
                                        color.darker_green,
                                        blocks=True, fighter=fighter_component,
                                        ai=ai_component)

            settings.objects.append(monster)

    num_items = libtcod.random_get_int(0, 0, max_items)

    for i in range(num_items):
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        if not Object.is_blocked(x, y):
            choice = random_choice(item_chances)
            if choice == 'heal':
                item_component = Item(use_function=spells.cast_heal)
                item = Object.Object(x, y, '!', 'healing potion',
                                     color.violet, item=item_component)
            elif choice == 'lightning':
                item_component = Item(use_function=spells.cast_lightning)
                item = Object.Object(x, y, '#', 'scroll of lightning bolt',
                                     color.light_yellow, item=item_component)
            elif choice == 'fireball':
                item_component = Item(use_function=spells.cast_fireball)
                item = Object.Object(x, y, '#', 'scroll of fireball',
                                     color.light_yellow, item=item_component)
            elif choice == 'confuse':
                item_component = Item(use_function=spells.cast_confuse)
                item = Object.Object(x, y, '#', 'scroll of confusion',
                                     color.light_yellow, item=item_component)
            elif choice == 'sword':
                equipment_component = Equipment(slot='right hand',
                                                power_bonus=3)
                item = Object.Object(x, y, '/', 'sword', color.sky,
                                     equipment=equipment_component)
            elif choice == 'shield':
                equipment_component = Equipment(slot='right hand',
                                                defense_bonus=1)
                item = Object.Object(x, y, '[', 'shield',
                                     color.darker_orange,
                                     equipment=equipment_component)
            settings.objects.append(item)
            item.send_to_back()
            item.always_visible = True


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


def from_dungeon_level(table):
    for (value, level) in reversed(table):
        if settings.dungeon_level >= level:
            return value
    return 0


def monster_death(monster):
    message('The ' + monster.name + ' is dead. You gain ' +
            str(monster.fighter.xp) + ' experiance points.',
            color.orange)
    monster.char = '%'
    monster.color = color.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()
