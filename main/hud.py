#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('HUD controller initialized.')

from sfml import Sprite, IntRect

from constants import PP_HEIGHT

class Hud(object):
    """HUD controller."""

    def __init__(self, player, background, faces, hudweapons, weapons, numbers):
        self.player = player

        self.background = Sprite(background)
        self.background.position = 0, PP_HEIGHT+1

        self.face = Sprite(faces)
        self.face.position = 116, 205
        self.face.scale = 2/3, 2/3

        self.hudweapon = Sprite(hudweapons)
        self.hudweapon.position = 251, 205

        self.weapon = Sprite(weapons)
        # self.weapon.position = 112, 105 #for x1.5
        # self.weapon.position = 96, 73 #for x2
        self.weapon.position = 104, 89
        self.weapon.scale = 1.75, 1.75

        self.deck_10 = Sprite(numbers)
        self.deck_10.position = 12, 223

        self.deck_1 = Sprite(numbers)
        self.deck_1.position = 25, 223

        self.score_1000 = Sprite(numbers)
        self.score_1000.position = 53, 223

        self.score_100 = Sprite(numbers)
        self.score_100.position = 67, 223

        self.score_10 = Sprite(numbers)
        self.score_10.position = 81, 223

        self.score_1 = Sprite(numbers)
        self.score_1.position = 95, 223

        self.hp_100 = Sprite(numbers)
        self.hp_100.position = 162, 223

        self.hp_10 = Sprite(numbers)
        self.hp_10.position = 176, 223

        self.hp_1 = Sprite(numbers)
        self.hp_1.position = 190, 223

        self.ammo_10 = Sprite(numbers)
        self.ammo_10.position = 214, 223

        self.ammo_1 = Sprite(numbers)
        self.ammo_1.position = 228, 223

        self.all_numbers = [self.deck_10, self.deck_1, self.score_1000,
            self.score_100, self.score_10, self.score_1, self.hp_100,
                self.hp_10, self.hp_1, self.ammo_10, self.ammo_1]

    def prepare(self):
        """Prepare all the data to be displayed."""

        #faces
        if self.player.hp == 0:
            self.face.texture_rect = IntRect(129, 0, 64, 64)
        elif self.player.hp > 0 and self.player.hp < 50:
            self.face.texture_rect = IntRect(65, 0, 64, 64)
        else:
            self.face.texture_rect = IntRect(0, 0, 64, 64)

        #hud weapons indicator
        if self.player.weapon.ident == 'rifle':
            self.hudweapon.texture_rect = IntRect(0, 85, 65, 42)
        elif self.player.weapon.ident == 'pistol':
            self.hudweapon.texture_rect = IntRect(0, 43, 65, 42)
        else:
            self.hudweapon.texture_rect = IntRect(0, 0, 65, 42)

        #in hand weapon indicator
        if self.player.attack == True:
            if self.player.weapon.ident == 'rifle':
                self.weapon.texture_rect = IntRect(64, 128, 64, 64)
            elif self.player.weapon.ident == 'pistol':
                self.weapon.texture_rect = IntRect(64, 64, 64, 64)
            else:
                self.weapon.texture_rect = IntRect(64, 0, 64, 64)

        else:
            if self.player.weapon.ident == 'rifle':
                self.weapon.texture_rect = IntRect(0, 128, 64, 64)
            elif self.player.weapon.ident == 'pistol':
                self.weapon.texture_rect = IntRect(0, 64, 64, 64)
            else:
                self.weapon.texture_rect = IntRect(0, 0, 64, 64)


        #numbers

        numbers(num_digits(2, self.player.deck), self.deck_10)
        numbers(num_digits(1, self.player.deck), self.deck_1)

        numbers(num_digits(4, self.player.score), self.score_1000)        
        numbers(num_digits(3, self.player.score), self.score_100)
        numbers(num_digits(2, self.player.score), self.score_10)
        numbers(num_digits(1, self.player.score), self.score_1)

        numbers(num_digits(3, self.player.hp), self.hp_100)
        numbers(num_digits(2, self.player.hp), self.hp_10)
        numbers(num_digits(1, self.player.hp), self.hp_1)

        numbers(num_digits(2, self.player.weapon.ammo), self.ammo_10)
        numbers(num_digits(1, self.player.weapon.ammo), self.ammo_1)

    def display(self, window):
        """Display the HUD with correct values."""

        self.prepare()
        
        window.draw(self.background)
        window.draw(self.face)
        window.draw(self.hudweapon)
        window.draw(self.weapon)        

        i = 0
        while i != len(self.all_numbers):
            window.draw(self.all_numbers[i])
            i += 1

def numbers(digit, sprite):
    """Change the sprite to the correct digit"""

    if digit == 0:
        sprite.texture_rect = IntRect(0, 0, 13, 20)
    else:
        sprite.texture_rect = IntRect((13 * digit)+1, 0, 13, 20)

def num_digits(pos, number):
    """Pull a digit from a number by certain position.

    pos = 3, 643 -> 6
    """

    lenght = len(str(number))
    if pos > lenght:
        return 0
    elif lenght == 1 and pos == 1:
        return number
    else:
        return int((number%(10**pos))/10**(pos-1))