import libtcodpy as libtcod
import settings


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options')

    header_height = libtcod.console_get_height_rect(settings.con, 0, 0, width,
                                                    settings.SCREEN_HEIGHT,
                                                    header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    window = libtcod.console_new(width, height)

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height,
                                  libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE,
                                 libtcod.LEFT, text)
        y += 1
        letter_index += 1

    x = settings.SCREEN_WIDTH / 2 - width / 2
    y = settings.SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    index = key.c - ord('a')
    if index >= 0 and index < len(options):
        return index
    return None


def msgbox(text, width=50):
    menu(text, [], width)


def main_menu():
    import Game
    img = libtcod.image_load('terminal12x12_gs_ro.png')

    while not libtcod.console_is_window_closed():
        libtcod.image_blit_2x(img, 0, 0, 0)

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, settings.SCREEN_WIDTH / 2,
                                 settings.SCREEN_HEIGHT / 2 - 4,
                                 libtcod.BKGND_NONE, libtcod.CENTER,
                                 'TutMut')
        libtcod.console_print_ex(0, settings.SCREEN_WIDTH / 2,
                                 settings.SCREEN_HEIGHT - 2,
                                 libtcod.BKGND_NONE, libtcod.CENTER,
                                 'by Akhier')

        choice = menu('', ['Play a new game',
                           'Continue last game', 'Quit'], 24)

        if choice == 0:
            Game.new_game()
            Game.play_game()
        if choice == 1:
            try:
                Game.load_game()
            except:
                msgbox('\n No saved game to load. \n', 24)
                continue
            Game.play_game()
        elif choice == 2:
            break


def inventory_menu(header):
    if len(settings.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in settings.inventory:
            text = item.name
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)

    index = menu(header, options, settings.INVENTORY_WIDTH)

    if index is None or len(settings.inventory) == 0:
        return None
    return settings.inventory[index].item
