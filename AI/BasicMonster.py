import libtcodpy as libtcod
import settings


class BasicMonster:

    def take_turn(self):
        global fov_map, player
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)

            elif player.fighter.hp > 0:
                monster.fighter.attack(player)
