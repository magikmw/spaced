#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Player initialized.')

from math import sin, cos, radians

class Player(object):
    """The player. Should be ok to reuse for the main thing
    """
    def __init__(self, gamemap, weapon, x=2, y=1, heading=0, deck = 1, hp = 100, score = 0):
        self.x = x #x and y are the grid coordinates
        self.y = y
        self.ux = x * 1.5 #ux and uy are the unit coordinates
        self.uy = y * 1.5
        self.heading = heading
        self.gamemap = gamemap
        self.deck = deck
        self.hp = hp
        self.weapon = weapon
        self.score = score
        self.attack = False
        self.body = None

    def turn(self, direction):
        self.heading += direction
        if self.heading < 0:
            self.heading += 360
        elif self.heading > 360:
            self.heading -= 360

    def move(self, momentum):
        dirx = -cos(radians(self.heading))
        diry = -sin(radians(self.heading))

        new_x = self.ux + momentum*dirx
        new_y = self.uy + momentum*diry

        if self.gamemap[(int(new_x),int(new_y))].blocked == False:
            self.ux += momentum*dirx
            self.uy += momentum*diry

            self.update_grid()

        # self.ux += int(dirx*momentum)
        # self.uy += int(diry*momentum)

    def strafe(self, momentum):
        if momentum < 0:
            heading = self.heading - 90

            dirx = -cos(radians(heading))
            diry = -sin(radians(heading))

        elif momentum > 0:
            heading = self.heading + 90

            dirx = cos(radians(heading))
            diry = sin(radians(heading))

        # if heading < 0:
        #     heading += 360

        new_x = self.ux + dirx*momentum
        new_y = self.uy + diry*momentum

        if self.gamemap[(int(new_x),int(new_y))].blocked == False:
            self.ux += dirx*momentum
            self.uy += diry*momentum

            self.update_grid()

    def update_grid(self):
        self.x = int(self.ux)
        self.y = int(self.uy)