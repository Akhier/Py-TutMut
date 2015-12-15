import libtcodpy as libtcod
import settings


class BasicMonster:

    def take_turn(self):
        monster = self.owner
        if libtcod.map_is_in_fov(settings.fov_map, monster.x, monster.y):
            if monster.distance_to(settings.player) >= 2:
                monster.move_towards(settings.player.x, settings.player.y)

            elif settings.player.fighter.hp > 0:
                monster.fighter.attack(settings.player)
