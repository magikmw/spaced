#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Entity class initialized.')

from sfml import IntRect, Sprite, Color

from math import sqrt, atan2, degrees, cos, radians

from constants import PP_HEIGHT, PP_WIDTH, PP_DISTANCE, FOV, ANGLE_SHIFT

class Entity(object):
    """Any and all entities that are displayed in the world.

    Barrels, enemies, goodies...
    """

    def __init__(self, x, y, texture, sprite_x, sprite_y):
        self.x = x
        self.y = y
        self.ux = x + .5
        self.uy = y + .5
        self.sprite = gen_sprite_slices(texture, sprite_x, sprite_y)
        self.distance = 0
        self.visible = False
        self.body = None

    def distance_to_player(self, player):
        self.distance = sqrt((player.ux - self.ux)**2 + (player.uy - self.uy)**2)

    def set_sprite_for_display(self, player, wall_distance):
        relative_ux = self.ux - player.ux
        relative_uy = self.uy - player.uy

        relative_angle = degrees(atan2(relative_uy, relative_ux)) + 180
        if relative_angle < 0:
            relative_angle += 360
        elif relative_angle >= 360:
            relative_angle -= 360

        temp = player.heading - relative_angle
        if temp < -90:
            temp = temp + 360
        elif temp > 90:
            temp = temp - 360

        # print(temp)

        screen_x = int(-((temp) * PP_WIDTH / FOV) + 160)
        # print(str(self.visible) + " " + str(round(screen_x, 2)))

        d = abs(int(self.distance * 64 * cos(radians(abs(-FOV/2 + ANGLE_SHIFT*(screen_x))))-.5))
        try:
            sprite_width = int((64 / d * PP_DISTANCE)+.5)
        except(ZeroDivisionError):
            sprite_width = int((64 / 1 * PP_DISTANCE)+.5)

        # print(str(screen_x) + ' ' + str(relative_angle))

        if 0 <= screen_x + sprite_width/2 < 359 or 0 <= screen_x - sprite_width/2 < 359:
            self.visible = True

            ix = 0
            if screen_x - sprite_width/2 < 0:
                texture_x = abs(screen_x - sprite_width/2)
            else:
                texture_x = 0

            # print(str(screen_x) + ' ' + str(sprite_width) + ' ' + str(texture_x))

            for sprite_slice in self.sprite:
                if screen_x - sprite_width/2 <= ix <= screen_x + sprite_width/2:
                    if self.distance < wall_distance[int(sprite_slice.x)]:
                        distance = abs(int(self.distance * 64 * cos(radians(abs(-FOV/2 + ANGLE_SHIFT*(sprite_slice.x))))-.5))
                        try:
                            height = int((64 / distance * PP_DISTANCE)+.5)
                        except(ZeroDivisionError):
                            height = int(64 * PP_DISTANCE+.5)
                        sprite_slice.y = PP_HEIGHT/2 - height/2
                        sprite_slice.set_texture_rect(IntRect(texture_x/(sprite_width/64), 0, 1, 64))
                        scale = height/64
                        sprite_slice.scale = (1, scale)
                        sprite_slice.color = Color.WHITE
                        texture_x += 1
                    else:
                        sprite_slice.color = Color.TRANSPARENT
                        texture_x += 1
                else:
                    sprite_slice.color = Color.TRANSPARENT

                ix += 1

        else:
            self.visible = False
            for sprite_slice in self.sprite:
                sprite_slice.color = Color.TRANSPARENT

    def update_position(self):
        self.x = int(self.body.position[0])
        self.y = int(self.body.position[1])
        self.ux = self.body.position[0]
        self.uy = self.body.position[1]

def gen_sprite_slices(texture, sprite_x, sprite_y):
    """Creates a list of 64 sprite slices to be scaled and displayed one by one.
    """

    sprite = []
    for i in range(PP_WIDTH):
        sprite_slice = Sprite(texture)
        sprite_slice.position = (i, PP_HEIGHT/2 - 32)
        sprite.append(sprite_slice)

    return sprite