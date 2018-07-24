import component as c
import const

import random
import tcod
import csv


class RandomMonster:
    def __init__(self):
        self.monsters = {}
        self._load_csv()

    def _load_csv(self):
        with open('data/monster.csv', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                row['fg'] = getattr(tcod, row['fg'])
                self.monsters[i] = row

    def generate(self, x, y):
        row = random.choice(self.monsters)
        return monster(
            name=row['name'],
            char=row['char'],
            fg=row['fg'],
            x=x,
            y=y
        )


def monster(name, char, fg, x, y):
    return (
        c.EnemyTurn(),
        c.Position(x=x, y=y),
        c.Movable(),
        c.Renderable(char=char, fg=fg),
        c.Collidable(),
        c.Describable(name=name),
        c.Stats(hp=10, defense=0, power=3),
        c.ExperienceModifier(),
    )


def player(x, y):
    return (
        c.PlayerTurn(),
        c.Position(x=x, y=y),
        c.Movable(),
        c.Renderable('@'),
        c.Collidable(),
        c.Describable(name='player'),
        c.Stats(max_hp=30, hp=30, defense=2, power=5),
        c.Inventory([]),
        c.Experience(),
    )


def stairs(x, y):
    return (
        c.Position(x=x, y=y),
        c.Renderable(char='>', fg=tcod.white, layer=const.LAYER_STAIRS),
        c.Describable(name='Stairs'),
        c.Enterable()
    )


def healing_potion(x, y):
    return (
        c.Position(x=x, y=y),
        c.Renderable(char='!', fg=tcod.fuchsia, layer=const.LAYER_ITEM),
        c.Describable(name='healing potion'),
        c.Carryable(),
        c.Consumable(),
        c.StatsModifier(hp=10)
    )


class RandomScroll:
    def __init__(self):
        self.scrolls = {}
        self._load_csv()

    def _load_csv(self):
        with open('data/scroll.csv', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                row['fg'] = getattr(tcod, row['fg'])
                self.scrolls[i] = row

    def generate(self, x, y):
        row = random.choice(self.scrolls)
        return scroll(
            name=row['name'],
            char=row['char'],
            fg=row['fg'],
            x=x,
            y=y
        )


def scroll(name='fireball', char='#', fg=tcod.red, x=0, y=0):
    return (
        c.Position(x=x, y=y),
        c.Renderable(char=char, fg=fg, layer=const.LAYER_ITEM),
        c.Describable(name=name),
        c.Carryable(),
        c.Aimable(),
        c.StatsModifier(hp=-200),
        c.StatusModifer(),
    )
