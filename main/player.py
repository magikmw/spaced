#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Player initialized.')

from math import sin, cos, radians, degrees

import Box2D as b2

class Player(object):
    """The player. Should be ok to reuse for the main thing
    """
    def __init__(self, gamemap, weapon, x=4, y=4, heading=180, deck = 1, hp = 100, score = 0):
        self.x = x #x and y are the grid coordinates
        self.y = y
        self.ux = x + .5 #ux and uy are the unit coordinates
        self.uy = y + .5
        self.heading = heading
        self.gamemap = gamemap
        self.deck = deck
        self.hp = hp
        self.weapon = weapon
        self.score = score
        self.attack = False
        self.attack_delay = 0
        self.body = None
        self.bob = 0
        self.strafing = False

    def turn(self, direction):
        self.heading += direction
        if self.heading < 0:
            self.heading += 360
        elif self.heading > 360:
            self.heading -= 360

    def move(self,momentum, direction):
        if direction == "forward":
            dirx = -cos(radians(self.heading))
            diry = -sin(radians(self.heading))

        elif direction == "backward":
            dirx = cos(radians(self.heading))
            diry = sin(radians(self.heading))            

        if self.strafing == True:
            force = b2.b2Vec2(dirx*momentum/2, diry*momentum/2)
        else:
            force = b2.b2Vec2(dirx*momentum, diry*momentum)

        self.body.ApplyLinearImpulse(force, self.body.position)

    def strafe(self, momentum, direction):
        if direction == "right":

            dirx = cos(radians(self.heading-90))
            diry = sin(radians(self.heading-90))

        elif direction == "left":

            dirx = cos(radians(self.heading+90))
            diry = sin(radians(self.heading+90))

        force = b2.b2Vec2(dirx*momentum, diry*momentum)

        self.body.ApplyLinearImpulse(force, self.body.position)

    def update_grid(self):
        self.x = int(self.ux)
        self.y = int(self.uy)

    def update_position(self):
        self.x = int(self.body.position[0])
        self.y = int(self.body.position[1])
        self.ux = self.body.position[0]
        self.uy = self.body.position[1]