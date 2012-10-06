#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Player initialized.')

from math import sin, cos, radians

class Player(object):
    """The player. Should be ok to reuse for the main thing
    """
    def __init__(self, gamemap, weapon, x=2, y=1, heading=270, deck = 1, hp = 100, score = 0):
        self.x = x #x and y are the grid coordinates
        self.y = y
        self.ux = x * 64 + 32 #ux and uy are the unit coordinates
        self.uy = y * 64 + 32
        self.heading = heading
        self.gamemap = gamemap
        self.deck = deck
        self.hp = hp
        self.weapon = weapon
        self.score = score
        self.attack = False

    def turn(self, direction):
        self.heading += direction
        if self.heading < 0:
            self.heading += 360
        elif self.heading > 360:
            self.heading -= 360

    def move(self, momentum):
        dirx = cos(radians(self.heading))
        diry = sin(radians(self.heading))

        new_x = self.ux + int(dirx*momentum)
        new_y = self.uy + int(diry*momentum)

        if self.gamemap[(int(new_x/64),int(new_y/64))].blocked == False:
            self.ux += int(dirx*momentum)
            self.uy += int(diry*momentum)

            self.update_grid()

        # self.ux += int(dirx*momentum)
        # self.uy += int(diry*momentum)

    def strafe(self, momentum):
        if momentum < 0:
            heading = self.heading - 90

            dirx = cos(radians(heading))
            diry = sin(radians(heading))

        elif momentum > 0:
            heading = self.heading + 90

            dirx = -cos(radians(heading))
            diry = -sin(radians(heading))

        # if heading < 0:
        #     heading += 360

        new_x = self.ux + int(dirx*momentum)
        new_y = self.uy + int(diry*momentum)

        if self.gamemap[(int(new_x/64),int(new_y/64))].blocked == False:
            self.ux += int(dirx*momentum)
            self.uy += int(diry*momentum)        

            self.update_grid()

    def update_grid(self):
        self.x = int(self.ux / 64)
        self.y = int(self.uy / 64)