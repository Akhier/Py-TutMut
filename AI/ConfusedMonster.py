import libtcodpy as libtcod
import message


class ConfusedMonster:

    def __init__(self, old_ai, num_turns=10):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            self.owner.move(libtcod.random_get_int(0, -1, 1),
                            libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
        elif self.num_turns == -1:
            self.owner.move(libtcod.random_get_int(0, -1, 1),
                            libtcod.random_get_int(0, -1, 1))
        else:
            self.owner.ai = self.old_ai
            message.message('The ' + self.owner.name +
                            ' is no longer confused.', libtcod.red)
