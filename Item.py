import settings
import message
import color
from Equipment import get_equipped_in_slot


class Item:

    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        if len(settings.inventory) >= 26:
            message.message('Your inventory is full, you cannot pick up ' +
                            self.owner.name + '.', color.red)
        else:
            settings.inventory.append(self.owner)
            settings.objects.remove(self.owner)
            message.message('You picked up a ' + self.owner.name + '.',
                            color.green)

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
        message.message('You dropped a ' + self.owner.name + '.', color.yellow)

    def use(self):
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return

        if self.use_function is None:
            message.message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                settings.inventory.remove(self.owner)
