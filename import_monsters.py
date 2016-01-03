import color
import glob
from Deaths import Death_type
from Fighter import Fighter
from Object import Object
from AI import AI_type


def import_monsters():
    monsters = {}
    monster = []
    processing = False
    part = ''
    for filename in glob.glob('Monsters/*.txt'):
        textfile = open(filename, 'r')
        if textfile.read(8) == 'MONSTERS':
            for c in textfile.read():
                if c == '{':
                    monster = []
                    processing = True
                if processing:
                    if c == '[':
                        part = ''
                    elif c == ']':
                        monster.append(part)
                    elif c == '}':
                        finishedmonster = make_monster(monster)
                        monsters[finishedmonster.name] = finishedmonster
                        processing = False
                    else:
                        part = part + c
    return monsters


def make_monster(parts):
    name = 'default'
    char = '@'
    colour = 'white'
    blocking = False
    fighter_component = None
    ai_component = None
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

    return Object(0, 0, char, name, getattr(color, colour),
                  blocks=blocking, fighter=fighter_component,
                  ai=AI_type[ai_component]())


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

    return Fighter(hp=_hp, defense=_defense, power=_power, xp=_xp,
                   death_function=Death_type[death_component])


monsters = import_monsters()


if __name__ == '__main__':
    monsterlist = import_monsters()
    for key in monsterlist:
        print(key)
