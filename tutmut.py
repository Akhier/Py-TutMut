import libtcodpy as libtcod
import settings
settings.init()


def main_menu():
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
            new_game()
            play_game()
        if choice == 1:
            try:
                load_game()
            except:
                msgbox('\n No saved game to load. \n', 24)
                continue
            play_game()
        elif choice == 2:
            break


if __name__ == '__main__':
    main_menu()
