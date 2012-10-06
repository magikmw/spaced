#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Weapons initialized.')

class Weapons(object):
    """Weapons to be used by the player."""

    def __init__(self, ident, ammo = 0, enabled = 0):
        self.ident = ident
        self.ammo = ammo
        self.enabled = enabled