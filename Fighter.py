import libtcodpy as libtcod
import settings
from message import message


class Fighter:

    global player

    def __init__(self, hp, defense, power, xp, death_function=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.death_function = death_function

    @property
    def power(self):
        bonus = sum(equipment.power_bonus for
                    equipment in get_all_equipped(self.owner))
        return self.base_power + bonus

    @property
    def defense(self):
        bonus = sum(equipment.defense_bonus for
                    equipment in get_all_equipped(self.owner))
        return self.base_defense + bonus

    @property
    def max_hp(self):
        bonus = sum(equipment.max_hp_bonus for
                    equipment in get_all_equipped(self.owner))
        return self.base_max_hp + bonus

    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            print(self.owner.name.capitalize() + ' attacks ' +
                  target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            print(self.owner.name.capitalize() + ' attacks ' +
                  target.name + ' but it has no effect.')

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner)
                if self.owner != player:
                    player.fighter.xp += self.xp

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp


def player_death(player):
    global game_state
    print('you died.')
    game_state = 'dead'

    player.char = '%'
    player.color = libtcod.dark_red


def monster_death(monster):
    message('The ' + monster.name + ' is dead. You gain ' +
            str(monster.fighter.xp) + ' experiance points.',
            libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()
