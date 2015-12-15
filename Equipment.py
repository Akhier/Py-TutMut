import libtcodpy as libtcod
import settings
from message import message


class Equipment:

    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.slot = slot
        self.is_equipped = False

    def toggle_equip(self):
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        old_equipment = get_equipped_in_slot(self.slot)
        if old_equipment is not None:
            old_equipment.dequip()

        self.is_equipped = True
        message('Equipped ' + self.owner.name + ' on ' +
                self.slot + '.', libtcod.light_green)

    def dequip(self):
        if not self.is_equipped:
            return
        self.is_equipped = False
        message('Dequipped ' + self.owner.name + ' from ' +
                self.slot + '.', libtcod.yellow)


def get_equipped_in_slot(slot):
    global inventory
    for obj in inventory:
        if (obj.equipment and obj.equipment.slot == slot and
                obj.equipment.is_equipped):
            return obj.equipment


def get_all_equipped(obj):
    global player
    if obj == player:
        equipped_list = []
        for item in inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list
    else:
        return []
