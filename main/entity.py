#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Entity class initialized.')

from sfml import IntRect

class Entity(object):
    """Any and all entities that are displayed in the world.

    Barrels, enemies, goodies...
    """

    def __init__(self, x, y, sprite, sprite_x, sprite_y):
        self.x = x
        self.y = y
        self.ux = x * 1.5
        self.uy = y * 1.5
        self.sprite = sprite
        self.sprite.set_texture_rect(IntRect(sprite_x, sprite_y, 64, 64))