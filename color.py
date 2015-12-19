import libtcodpy as libtcod


dark_wall = libtcod.Color(0, 0, 100)
light_wall = libtcod.Color(130, 110, 50)
dark_ground = libtcod.Color(50, 50, 150)
light_ground = libtcod.Color(200, 180, 50)
white = libtcod.white   # settings~player, settings~stairs
# message default message color, menu default foreground,
# Object.clear, render_all floor, render_all wall,
# render_all default foreground, render_all~render_bar default foreground
light_green = libtcod.light_green   # Equipment.equip message,
# spells~cast_confuse success message
yellow = libtcod.yellow   # Equipment.dequip message
# Item.drop dropped item message, player_game.check_level_up level up message
light_violet = libtcod.light_violet   # handle_keys~next_level heal message,
# spells~cast_heal heal message
red = libtcod.red   # handle_keys~next_level descending message,
# Item.pick_up full inventory message, new_game welcome message,
# spells~cast_heal full health message, spells~cast_lightning no target message
green = libtcod.green   # Item.pick_up item pick up message
sky = libtcod.sky   # new_game dagger, place_objects sword
dark_red = libtcod.dark_red   # new_game~player_death dead player
desaturated_green = libtcod.desaturated_green   # place_objects orc
darker_green = libtcod.darker_green   # place_objects troll
violet = libtcod.violet   # place_objects healing potion
light_yellow = libtcod.light_yellow   # place_objects scroll of lightning bolt
# place_objects scroll of fireball, place_objects scroll of confusion,
# tutmut default foreground
darker_orange = libtcod.darker_orange   # place_objects shield
orange = libtcod.orange   # place_objects~monster_death death message,
# spells~cast_fireball area message, spells~cast_fireball hit message
dark_red = libtcod.dark_orange   # place_objects~monster_death corpse
black = libtcod.black   # render_all default background
light_red = libtcod.light_red   # render_all health bar
darker_red = libtcod.darker_red   # render_all health bar
light_gray = libtcod.light_gray   # render_all default foreground
light_blue = libtcod.light_blue   # spells~cast_lightning hit message
light_cyan = libtcod.light_cyan   # spells~cast_fireball targeting message,
# spells~cast_confuse targeting message
