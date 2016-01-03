import color
from message import message


def basic_death(monster):
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
