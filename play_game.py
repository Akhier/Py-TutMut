import libtcodpy as libtcod
import settings
from handle_keys import handle_keys
from render_all import render_all
from save_game import save_game
from message import message
from menu import menu


def play_game():
    settings.player_action = None
    settings.mouse = libtcod.Mouse()
    settings.key = libtcod.Key()
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS |
                                    libtcod.EVENT_MOUSE,
                                    settings.key, settings.mouse)
        render_all()
        libtcod.console_flush()
        check_level_up()

        for object in settings.objects:
            object.clear()

        settings.player_action = handle_keys()
        if settings.player_action == 'exit':
            save_game()
            break

        if settings.game_state == 'playing' and \
           settings.player_action != 'didnt-take-turn':
            for object in settings.objects:
                if object.ai:
                    object.ai.take_turn()


def check_level_up():
    level_up_xp = settings.LEVEL_UP_BASE + settings.player.level * \
        settings.LEVEL_UP_FACTOR
    if settings.player.fighter.xp >= level_up_xp:
        settings.player.level += 1
        settings.player.fighter.xp -= level_up_xp
        message('Your battle skills grow stronger. You reached level ' +
                str(settings.player.level) + '.', libtcod.yellow)

        choice = None
        while choice is None:
            choice = menu('Level up! Choose a stat to raise:\n',
                          ['Constitution (+20 HP, from ' +
                           str(settings.player.fighter.max_hp) + ')',
                           'Strength (+1 attack, from ' +
                           str(settings.player.fighter.power) + ')',
                           'Agility (+1 defense, from ' +
                           str(settings.player.fighter.defense) + ')'],
                          settings.LEVEL_SCREEN_WIDTH)

        if choice == 0:
            settings.player.fighter.max_hp += 20
            settings.player.fighter.hp += 20
        elif choice == 1:
            settings.player.fighter.power += 1
        elif choice == 2:
            settings.player.fighter.defense += 1
