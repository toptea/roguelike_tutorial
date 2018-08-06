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
                row['exp'] = int(row['exp'])
                row['hp'] = int(row['hp'])
                row['defense'] = int(row['defense'])
                row['power'] = int(row['power'])
                self.monsters[i] = row

    def generate(self, x, y):
        row = random.choice(self.monsters)
        return monster(
            name=row['name'],
            char=row['char'],
            fg=row['fg'],
            x=x,
            y=y,
            xp=row['exp'],
            hp=row['hp'],
            defense=row['defense'],
            power=row['power']
        )


def monster(name, char, fg, x, y, xp, hp, defense, power):
    return (
        c.EnemyTurn(),
        c.Position(x=x, y=y),
        c.Movable(),
        c.Renderable(char=char, fg=fg),
        c.Collidable(),
        c.Describable(name=name),
        c.Stats(hp=hp, max_hp=hp, defense=defense, power=power),
        c.Status(),
        c.ExperienceModifier(xp=xp),
    )


def player(x, y):
    return (
        c.PlayerTurn(),
        c.Position(x=x, y=y),
        c.Movable(),
        c.Renderable('@'),
        c.Collidable(),
        c.Describable(name='player'),
        c.Stats(max_hp=1000, hp=1000, defense=1, power=5),
        c.Status(),
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


class RandomItem:
    def __init__(self):
        self.scrolls = {}
        self._load_csv()

    def _load_csv(self):
        with open('data/item.csv', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                row['countdown'] = int(row['countdown'])
                row['confuse'] = bool(int(row['confuse']))
                row['paralyse'] = bool(int(row['paralyse']))
                row['freeze'] = bool(int(row['freeze']))
                row['burn'] = bool(int(row['burn']))
                row['hp'] = int(row['hp'])
                row['fg'] = getattr(tcod, row['fg'])
                self.scrolls[i] = row

    def generate(self, x, y):
        row = random.choice(self.scrolls)
        return item(
            name=row['name'],
            char=row['char'],
            fg=row['fg'],
            x=x,
            y=y,
            countdown=row['countdown'],
            confuse=row['confuse'],
            paralyse=row['paralyse'],
            freeze=row['freeze'],
            burn=row['burn'],
            hp=row['hp']
        )


def item(name, char, fg, x, y, countdown, confuse, paralyse, freeze, burn, hp):
    return (
        c.Position(x=x, y=y),
        c.Renderable(char=char, fg=fg, layer=const.LAYER_ITEM),
        c.Describable(name=name),
        c.Carryable(),
        c.Aimable(),
        c.StatsModifier(hp=hp),
        c.StatusModifier(
            countdown=countdown,
            confuse=confuse,
            paralyse=paralyse,
            freeze=freeze,
            burn=burn,
        ),
    )
