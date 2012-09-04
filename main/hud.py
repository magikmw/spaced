#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('HUD controller initialized.')

from sfml import Sprite, IntRect

from constants import PP_HEIGHT

class Hud(object):
    """HUD controller."""

    def __init__(self, player, background, faces, weapons):
        self.player = player

        self.background = Sprite(background)
        self.background.position = 0, PP_HEIGHT+1

        self.face_full = Sprite(faces)
        self.face_full.texture_rect = IntRect(0, 0, 64, 64)
        self.face_full.position = 116, 205
        self.face_full.scale = 2/3, 2/3

        self.face_hurt = Sprite(faces)
        self.face_hurt.texture_rect = IntRect(65, 0, 64, 64)
        self.face_hurt.position = 116, 205
        self.face_hurt.scale = 2/3, 2/3

        self.face_dead = Sprite(faces)
        self.face_dead.texture_rect = IntRect(129, 0, 64, 64)
        self.face_dead.position = 116, 205
        self.face_dead.scale = 2/3, 2/3

        self.knife = Sprite(weapons)
        self.knife.texture_rect = IntRect(0, 0, 65, 42)
        self.knife.position = 251, 205

        self.pistol = Sprite(weapons)
        self.pistol.texture_rect = IntRect(0, 43, 65, 42)
        self.pistol.position = 251, 205

        self.rifle = Sprite(weapons)
        self.rifle.texture_rect = IntRect(0, 85, 65, 42)
        self.rifle.position = 251, 205

    def display():
        """This should be used in the display part of main loop to... display the HUD with correct values."""
        
        pass


#face high left corner - 116,4 + 0,200