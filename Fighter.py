import settings


class Fighter:

    def __init__(self, hp, defense, power, xp, death_function=None):
        self.base_max_hp = int(hp)
        self.hp = int(hp)
        self.base_defense = int(defense)
        self.base_power = int(power)
        self.xp = int(xp)
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
                if self.owner != settings.player:
                    settings.player.fighter.xp += self.xp

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp


def get_all_equipped(obj):
    if obj == settings.player:
        equipped_list = []
        for item in settings.inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list
    else:
        return []
