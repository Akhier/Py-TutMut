import settings
import Object
import copy
from import_monsters import monsters, packs
from import_items import items


def place_objects(rect):
    max_monster = from_dungeon_level([[2, 1], [3, 4], [5, 6]])

    monster_chances = {}
    for key in monsters:
        monster_chances[key] = \
            from_dungeon_level(monsters[key].placement_range)

    max_items = from_dungeon_level([[1, 1], [2, 4]])

    item_chances = {}
    for key in items:
        item_chances[key] = from_dungeon_level(items[key].placement_range)

    num_monsters = settings.RNG.get_int(0, max_monster)

    for i in range(num_monsters):
        x = settings.RNG.get_int(rect.x1 + 1, rect.x2 - 1)
        y = settings.RNG.get_int(rect.y1 + 1, rect.y2 - 1)

        if not Object.is_blocked(x, y):
            choice = random_choice(monster_chances)
            monster = copy.deepcopy(monsters[choice])
            monster.x = x
            monster.y = y
            if choice in packs:
                place_pack(monster)
            settings.objects.append(monster)

    num_items = settings.RNG.get_int(0, max_items)

    for i in range(num_items):
        x = settings.RNG.get_int(rect.x1 + 1, rect.x2 - 1)
        y = settings.RNG.get_int(rect.y1 + 1, rect.y2 - 1)

        if not Object.is_blocked(x, y):
            choice = random_choice(item_chances)
            item = copy.deepcopy(items[choice])
            item.x = x
            item.y = y
            settings.objects.append(item)
            item.send_to_back()
            item.always_visible = True


def place_pack(monster):
    (min, max) = packs[monster.name]
    cur_x = monster.x
    cur_y = monster.y
    failures = 0
    monsters_to_place = settings.RNG.get_int(min, max) - 1
    while monsters_to_place > 0:
        x = cur_x + settings.RNG.get_int(-1, 1)
        y = cur_y + settings.RNG.get_int(-1, 1)
        if not Object.is_blocked(x, y):
            packmonster = copy.deepcopy(monster)
            packmonster.x = x
            packmonster.y = y
            settings.objects.append(packmonster)
            cur_x = x
            cur_y = y
            monsters_to_place -= 1
            failures = 0
        else:
            failures += 1
            if failures > 10:
                cur_x = monster.x
                cur_y = monster.y
            if failures > 30:
                monsters_to_place -= 1


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
