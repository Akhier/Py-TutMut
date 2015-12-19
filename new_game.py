import handle_keys
import settings
import color
from Equipment import Equipment
from make_map import make_map
from Fighter import Fighter
from message import message
from Object import Object


def new_game():
    fighter_component = Fighter(hp=30, defense=2, power=5,
                                xp=0, death_function=player_death)
    settings.player = Object(0, 0, '@', 'player', color.white, blocks=True,
                             fighter=fighter_component)

    settings.player.level = 1
    settings.dungeon_level = 1
    make_map()
    handle_keys.initialize_fov()
    settings.game_state = 'playing'
    settings.inventory = []
    settings.game_msgs = []

    message('Welcome stranger. Prepare to perish in the ' +
            'Tombs of the Ancient Kings.', color.red)
    equipment_component = Equipment(slot='right hand', power_bonus=2)
    obj = Object(0, 0, '-', 'dagger', color.sky,
                 equipment=equipment_component)
    settings.inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True


def player_death(player):
    print('you died.')
    settings.game_state = 'dead'
    settings.player.char = '%'
    settings.player.color = color.dark_red
