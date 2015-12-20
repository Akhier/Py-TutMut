class Rect:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.w = w
        self.h = h

    @property
    def x2(self):
        return self.x1 + self.w

    @property
    def y2(self):
        return self.y1 + self.h

    @property
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def move(self, x, y):
        self.x1 = x
        self.y1 = y

    def move_by_center(self, x, y):
        self.x1 = x - self.w / 2
        self.y1 = y - self.h / 2
