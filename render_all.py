import libtcodpy as libtcod
import settings


def render_all():
    if settings.fov_recompute:
        settings.fov_recompute = False
        libtcod.map_compute_fov(settings.fov_map, settings.player.x,
                                settings.player.y, settings.TORCH_RADIUS,
                                settings.FOV_LIGHT_WALLS, settings.FOV_ALGO)
        for y in range(settings.MAP_HEIGHT):
            for x in range(settings.MAP_WIDTH):
                visible = libtcod.map_is_in_fov(settings.fov_map, x, y)
                wall = settings.map[x][y].block_sight
                if not visible:
                    if settings.map[x][y].explored:
                        if wall:
                            libtcod.console_put_char_ex(settings.con,
                                                        x, y, '#',
                                                        libtcod.white,
                                                        settings.color_dark_wall)
                        else:
                            libtcod.console_put_char_ex(settings.con,
                                                        x, y, '.',
                                                        libtcod.white,
                                                        settings.color_dark_ground)
                else:
                    if wall:
                        libtcod.console_put_char_ex(settings.con, x, y, '#',
                                                    libtcod.white,
                                                    settings.color_light_wall)
                    else:
                        libtcod.console_put_char_ex(settings.con, x, y, '.',
                                                    libtcod.white,
                                                    settings.color_light_ground)
                    settings.map[x][y].explored = True

    for object in settings.objects:
        if object != settings.player:
            object.draw()
    settings.player.draw()

    libtcod.console_blit(settings.con, 0, 0, settings.SCREEN_WIDTH,
                         settings.SCREEN_HEIGHT, 0, 0, 0)

    libtcod.console_set_default_background(settings.panel, libtcod.black)
    libtcod.console_clear(settings.panel)

    y = 1
    for (line, color) in settings.game_msgs:
        libtcod.console_set_default_foreground(settings.panel, color)
        libtcod.console_print_ex(settings.panel, settings.MSG_X,
                                 y, libtcod.BKGND_NONE,
                                 libtcod.LEFT, line)
        y += 1

    render_bar(1, 1, settings.BAR_WIDTH, 'HP', settings.player.fighter.hp,
               settings.player.fighter.max_hp, libtcod.light_red,
               libtcod.darker_red)
    libtcod.console_print_ex(settings.panel, 1, 3, libtcod.BKGND_NONE,
                             libtcod.LEFT, 'Dungeon level ' +
                             str(settings.dungeon_level))

    libtcod.console_set_default_foreground(settings.con, libtcod.white)
    libtcod.console_print_ex(0, 1, settings.SCREEN_HEIGHT - 2,
                             libtcod.BKGND_NONE, libtcod.LEFT, 'HP: ' +
                             str(settings.player.fighter.hp) +
                             '/' + str(settings.player.fighter.max_hp))

    libtcod.console_set_default_foreground(settings.panel, libtcod.light_gray)
    libtcod.console_print_ex(settings.panel, 1, 0, libtcod.BKGND_NONE,
                             libtcod.LEFT, get_name_under_mouse())

    libtcod.console_blit(settings.panel, 0, 0, settings.SCREEN_WIDTH,
                         settings.PANEL_HEIGHT, 0, 0, settings.PANEL_Y)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(settings.panel, back_color)
    libtcod.console_rect(settings.panel, x, y, total_width, 1,
                         False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(settings.panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(settings.panel, x, y, bar_width, 1,
                             False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(settings.panel, libtcod.white)
    libtcod.console_print_ex(settings.panel, x + total_width / 2, y,
                             libtcod.BKGND_NONE, libtcod.CENTER,
                             name + ': ' + str(value) + '/' + str(maximum))


def get_name_under_mouse():
    (x, y) = (settings.mouse.cx, settings.mouse.cy)
    names = [obj.name for obj in settings.objects if obj.x == x and
             obj.y == y and libtcod.map_is_in_fov(settings.fov_map,
                                                  obj.x, obj.y)]
    names = ', '.join(names)
    return names.capitalize()
