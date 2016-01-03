import settings
import Object
import spells
import color
import copy
from import_monsters import monsters
from Equipment import Equipment
from Item import Item


def place_objects(rect):
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

    num_monsters = settings.RNG.get_int(0, max_monster)

    for i in range(num_monsters):
        x = settings.RNG.get_int(rect.x1 + 1, rect.x2 - 1)
        y = settings.RNG.get_int(rect.y1 + 1, rect.y2 - 1)

        if not Object.is_blocked(x, y):
            choice = random_choice(monster_chances)
            monster = copy.deepcopy(monsters[choice])
            monster.x = x
            monster.y = y
            settings.objects.append(monster)

    num_items = settings.RNG.get_int(0, max_items)

    for i in range(num_items):
        x = settings.RNG.get_int(rect.x1 + 1, rect.x2 - 1)
        y = settings.RNG.get_int(rect.y1 + 1, rect.y2 - 1)

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
    dice = settings.RNG.get_int(1, sum(chances))

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
