import libtcodpy as libtcod


class rng():

    def __init__(self, seed=12271990):
        self.rnd = libtcod.random_new_from_seed(seed, algo=libtcod.RNG_MT)

    def roll(self, num, sides):
        total = 0
        for dice in range(num):
            total += libtcod.random_get_int(self.rnd, 1, sides)

        return total

    def get_int(self, min, max):
        return libtcod.random_get_int(self.rnd, min, max)


if __name__ == '__main__':
    test = rng()
    line = 'rng()    '
    for i in range(3):
        line = line + str(test.roll(3, 6)) + ' ' + \
            str(test.get_int(3, 6)) + ' '

    test = rng(123)
    line = line + '\nrng(123) '
    for i in range(3):
        line = line + str(test.roll(3, 6)) + ' ' + \
            str(test.get_int(3, 6)) + ' '

    test = rng()
    line = line + '\nrng()    '
    for i in range(3):
        line = line + str(test.roll(3, 6)) + ' ' + \
            str(test.get_int(3, 6)) + ' '

    print(line)
