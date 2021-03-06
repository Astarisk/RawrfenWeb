class Coord:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0} {1})".format(self.x, self.y)

    def __repr__(self):
        return "Coord({0} , {1})".format(self.x, self.y)

    def mul(self, f):
        return Coord(self.x * f.x, self.y * f.y)


class Coord2d:
    def __int__(self):
        pass
