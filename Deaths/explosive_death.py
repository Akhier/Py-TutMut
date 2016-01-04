import spells
import color
import AI
from message import message


def explosive_death(monster):
    message('The ' + monster.name + ' is dead. You gain ' +
            str(monster.fighter.xp) + ' experiance points.',
            color.orange)
    monster.char = '*'
    monster.color = color.orange
    monster.blocks = False
    monster.fighter = None
    monster.ai = AI.CountDown(spells.cast_self_destruct)
    monster.ai.owner = monster
    monster.name = 'explosive remains of ' + monster.name
