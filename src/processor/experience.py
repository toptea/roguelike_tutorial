import component as c
import const
import esper
import tcod


class Experience(esper.Processor):
    scene = None

    def __init__(self):
        super().__init__()

    def get_experience(self):
        player = self.world.get_components(
            c.PlayerTurn,
            c.Experience
        )

        enemy = self.world.get_components(
            c.EnemyTurn,
            c.Stats,
            c.ExperienceModifier,
        )
        for _, (_, exp) in player:
            for _, (_, enemy_stats, exp_mod) in enemy:
                if enemy_stats.hp <= 0:
                    yield exp, exp_mod

    def process(self, *args):
        for exp, experience_mod in self.get_experience():
            exp.xp += experience_mod.xp

            self.scene.message.append(
                ('You gain {0} experience points.'.format(exp.xp), tcod.yellow)
            )

            if exp.xp > exp.xp_to_next_level:
                exp.xp -= exp.xp_to_next_level
                exp.level += 1
                self.scene.action = {'level_up': True}
                self.scene.message.append(
                    (
                        'Your battle skills grow stronger! You reached level {0}'.format(
                            exp.level
                        ),
                        tcod.yellow
                    )
                )
