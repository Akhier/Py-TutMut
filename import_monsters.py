import color
import glob
from Deaths import Death_type
from Fighter import Fighter
from Object import Object
from AI import AI_type


def import_monsters():
    monsters = {}
    monster = []
    packs = {}
    processing = False
    direct_read = False
    part = ''
    for filename in glob.glob('Monsters/*.txt'):
        textfile = open(filename, 'r')
        if textfile.read(8) == 'MONSTERS':
            for c in textfile.read():
                if c == '{' and not processing:
                    monster = []
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
                        monster.append(part)
                    elif c == '}':
                        finishedmonster = make_monster(monster)
                        packsize = check_if_pack(monster)
                        if packsize:
                            packs[finishedmonster.name] = packsize
                        monsters[finishedmonster.name] = finishedmonster
                        processing = False
                    else:
                        part = part + c
    return monsters, packs


def make_monster(parts):
    name = 'default'
    char = '@'
    colour = 'white'
    blocking = False
    fighter_component = None
    ai_component = None
    placement_range_component = None
    for p in parts:
        if p.startswith('name'):
            name = p.split('=', 1)[1]
        elif p.startswith('char'):
            char = p[-1:]
        elif p.startswith('color'):
            colour = p.split('=', 1)[1]
        elif p == 'blocks':
            blocking = True
        elif p.startswith('fighter'):
            piece = ''
            pieces = []
            for c in p:
                if c == '<':
                    piece = ''
                elif c == '>':
                    pieces.append(piece)
                else:
                    piece = piece + c

            fighter_component = make_fighter(pieces)
        elif p.startswith('ai'):
            ai_component = p.split('=', 1)[1]
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
                  blocks=blocking, fighter=fighter_component,
                  ai=AI_type[ai_component](),
                  placement_range=placement_range_component)


def make_fighter(pieces):
    _hp = 0
    _defense = 0
    _power = 0
    _xp = 0
    death_component = 'basic_death'
    for p in pieces:
        if p.startswith('hp'):
            _hp = p.split('=', 1)[1]
        elif p.startswith('def'):
            _defense = p.split('=', 1)[1]
        elif p.startswith('pow'):
            _power = p.split('=', 1)[1]
        elif p.startswith('xp'):
            _xp = p.split('=', 1)[1]
        elif p.startswith('death'):
            death_component = p.split('=', 1)[1]

    return Fighter(hp=int(_hp), defense=int(_defense),
                   power=int(_power), xp=int(_xp),
                   death_function=Death_type[death_component])


def make_placement_range(pieces):
    placement_range_component = []
    for p in pieces:
        s = p.split(':')
        placement_range_component.append([int(s[1]), int(s[0])])

    return placement_range_component


def check_if_pack(parts):
    for p in parts:
        if p.startswith('pack'):
            s = p.split('=')[1].split(':')
            i = [int(s[0]), int(s[1])]
            return i

    return False


(monsters, packs) = import_monsters()


if __name__ == '__main__':
    monsterlist = import_monsters()
    for key in monsterlist:
        print(key)
