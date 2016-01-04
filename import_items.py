import spells
import color
import glob
from Equipment import Equipment
from Object import Object
from Item import Item


def import_items():
    items = {}
    item = []
    processing = False
    direct_read = False
    part = ''
    for filename in glob.glob('Items/*.txt'):
        textfile = open(filename, 'r')
        if textfile.read(5) == 'ITEMS':
            for c in textfile.read():
                if c == '{' and not processing:
                    item = []
                    processing = True
                if processing:
                    if c == '\\' and not direct_read:
                        direct_read = True
                    elif direct_read:
                        part = part + c
                        direct_read = False
                    elif c == '[':
                        part = ''
                    elif c == ']':
                        item.append(part)
                    elif c == '}':
                        finisheditem = make_item(item)
                        items[finisheditem.name] = finisheditem
                        processing = False
                    else:
                        part = part + c
    return items


def make_item(parts):
    name = 'default'
    char = '@'
    colour = 'white'
    equipment_component = None
    placement_range_component = None
    use_component = None
    for p in parts:
        if p.startswith('name'):
            name = p.split('=', 1)[1]
        elif p.startswith('char'):
            char = p[-1:]
        elif p.startswith('color'):
            colour = p.split('=', 1)[1]
        elif p.startswith('use'):
            use_component = Item(use_function=getattr(spells,
                                                      p.split('=', 1)[1]))
        elif p.startswith('equipment'):
            piece = ''
            pieces = []
            for c in p:
                if c == '<':
                    piece = ''
                elif c == '>':
                    pieces.append(piece)
                else:
                    piece = piece + c

            equipment_component = make_equipment(pieces)
        elif p.startswith('placement'):
            piece = ''
            pieces = []
            for c in p:
                if c == '<':
                    piece = ''
                elif c == '>':
                    pieces.append(piece)
                else:
                    piece = piece + c

            placement_range_component = make_placement_range(pieces)

    return Object(0, 0, char, name, getattr(color, colour),
                  item=use_component, equipment=equipment_component,
                  placement_range=placement_range_component)


def make_equipment(pieces):
    _slot = 'Test'
    _power_bonus = 0
    _defense_bonus = 0
    _max_hp_bonus = 0
    for p in pieces:
        if p.startswith('slot'):
            _slot = p.split('=', 1)[1]
        elif p.startswith('power_bonus'):
            _power_bonus = p.split('=', 1)[1]
        elif p.startswith('defense_bonus'):
            _defense_bonus = p.split('=', 1)[1]
        elif p.startswith('max_hp_bonus'):
            _max_hp_bonus = p.split('=', 1)[1]

    return Equipment(_slot, power_bonus=int(_power_bonus),
                     defense_bonus=int(_defense_bonus),
                     max_hp_bonus=int(_max_hp_bonus))


def make_placement_range(pieces):
    placement_range_component = []
    for p in pieces:
        s = p.split(':')
        placement_range_component.append([int(s[1]), int(s[0])])

    return placement_range_component


items = import_items()


if __name__ == '__main__':
    itemlist = import_items()
    for key in itemlist:
        print(key)
