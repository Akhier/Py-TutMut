import libtcodpy as libtcod
import settings
from message import message
from Equipment import get_equipped_in_slot


class Item:

    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        if len(settings.inventory) >= 26:
            message('Your inventory is full, you cannot pick up ' +
                    self.owner.name + '.', libtcod.red)
        else:
            settings.inventory.append(self.owner)
            settings.objects.remove(self.owner)
            message('You picked up a ' + self.owner.name + '.', libtcod.green)

            equipment = self.owner.equipment
            if equipment and get_equipped_in_slot(equipment.slot) is None:
                equipment.equip()

    def drop(self):
        if self.owner.equipment:
            self.owner.equipment.dequip()

        settings.objects.append(self.owner)
        settings.inventory.remove(self.owner)
        self.owner.x = settings.player.x
        self.owner.y = settings.player.y
        message('You dropped a ' + self.owner.name + '.', libtcod.yellow)

    def use(self):
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                settings.inventory.remove(self.owner)
