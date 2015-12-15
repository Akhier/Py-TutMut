class Object:

    def __init__(self, x, y, char, name, color, blocks=False,
                 always_visible=False, fighter=None, ai=None,
                 item=None, equipment=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            self.item = Item()
            self.item.owner = self

    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def send_to_back(self):
        global objects
        objects.remove(self)
        objects.insert(0, self)

#    def draw(self):
#        if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
#                (self.always_visible and map[self.x][self.y].explored)):
#            libtcod.console_set_default_foreground(con, self.color)
#            libtcod.console_put_char(con, self.x, self.y, self.char,
#                                     libtcod.BKGND_NONE)

#    def clear(self):
#        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
#            libtcod.console_put_char_ex(con, self.x, self.y, '.',
#                                        libtcod.white, color_light_ground)
