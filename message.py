import libtcodpy as libtcod
import textwrap
import settings


def message(new_msg, color=libtcod.white):
    global game_msgs
    new_msg_lines = textwrap.wrap(new_msg, settings.MSG_WIDTH)

    for line in new_msg_lines:
        if len(game_msgs) == settings.MSG_HEIGHT:
            del game_msgs[0]

        game_msgs.append((line, color))
