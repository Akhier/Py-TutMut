import message
import color


class CountDown:

    def __init__(self, result, num_turns=3):
        self.result = result
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:
            message.message('The ' + self.owner.name +
                            '\'s timer is at ' + str(self.num_turns),
                            color.red)
            self.num_turns -= 1
        else:
            self.result(self)
            self.owner.ai = None
