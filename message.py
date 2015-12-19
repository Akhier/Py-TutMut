import textwrap
import settings
import color


def message(new_msg, color=color.white):
    new_msg_lines = textwrap.wrap(new_msg, settings.MSG_WIDTH)

    for line in new_msg_lines:
        if len(settings.game_msgs) == settings.MSG_HEIGHT:
            del settings.game_msgs[0]

        settings.game_msgs.append((line, color))
