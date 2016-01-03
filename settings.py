import libtcodpy as libtcod
import color
from Object import Object
from Tile import Tile
from rng import rng

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 43

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50
CHARACTER_SCREEN_WIDTH = 30
LEVEL_SCREEN_WIDTH = 40

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

HEAL_AMOUNT = 40
LIGHTNING_DAMAGE = 40
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 25

LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

LIMIT_FPS = 20

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

dungeon_level = 1
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
fov_recompute = True
game_msgs = []
game_state = 'start_up'
inventory = []
key = libtcod.Key()
map = [[Tile(True) for y in range(MAP_HEIGHT)]
       for x in range(MAP_WIDTH)]
flood_map = [[-1 for y in range(MAP_HEIGHT)]
             for x in range(MAP_WIDTH)]
mouse = libtcod.Mouse()
objects = []
player = Object(0, 0, '@', 'player', color.white)
stairs = Object(0, 0, '<', 'stairs', color.white)

RNG = rng()


def init():
    libtcod.console_set_custom_font('terminal12x12_gs_ro.png',
                                    libtcod.FONT_TYPE_GREYSCALE |
                                    libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                              'basicroguelike', False)
    libtcod.sys_set_fps(LIMIT_FPS)
