#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Raycaster initialized.')

from math import cos, sin, radians
from sfml import IntRect, Color
from constants import PP_DISTANCE, ANGLE_SHIFT, FOV, PP_WIDTH, PP_HEIGHT

class Raycaster(object):
    """The main raycasting class.

    Instance with a list of sprites, map and the player instance"""

    def __init__(self, player, sprites, gamemap):
        self.player = player
        self.sprites = sprites
        self.gamemap = gamemap

    def cast_rays(self):
        alpha = self.player.heading - FOV/2
        if alpha < 0:
            alpha += 360
        columns = []

        for index in range(PP_WIDTH):
            #figure out the vector from the angle
            dx = cos(radians(alpha))
            dy = sin(radians(alpha))

            #set the tdx and tdy according to the direction of the vector
            if dx > 0:
                tdx = -1
            elif dx < 0:
                tdx = 1
            else:
                tdx = 0

            if dy > 0:
                tdy = -1
            elif dy < 0:
                tdy = 1
            else:
                tdy = 0

            #reset the vector to absolute values
            dx = abs(dx)
            dy = abs(dy)

            try:
                tick_x = 1/dx
            except(ZeroDivisionError):
                tick_x = 1

            try:
                tick_y = 1/dy
            except(ZeroDivisionError):
                tick_y = 1

            #calculate the cx and cy
            if tdx == 1:
                # cx = (1 - (self.player.ux % 64)/64) * tick_x
                cx = (1 - (self.player.ux - self.player.x)) * tick_x
            elif tdx == -1:
                # cx = ((self.player.ux % 64)/64) * tick_x
                cx = (self.player.ux - self.player.x) * tick_x
            else:
                cx = 9999999999999999999999999999999999
                #don't use bigger maps than that

            if tdy == 1:
                # cy = (1 - (self.player.uy % 64)/64) * tick_y
                cy = (1 - (self.player.uy - self.player.y)) * tick_y
            elif tdy == -1:
                # cy = ((self.player.uy % 64)/64) * tick_y
                cy = (self.player.uy - self.player.y) * tick_y
            else:
                cy = 9999999999999999999999999999999999
                #don't use bigger maps than that

            #figure out which one is 'faster'

            distance = 0
            shading = False
            origin_x = self.player.x
            origin_y = self.player.y

            while True:
                if cy < cx:
                    distance += cy
                    if self.gamemap[(origin_x, origin_y + tdy)].skin != None:
                        if self.gamemap[(origin_x, origin_y + tdy)].door and 0>1:
                            P = self.gamemap[(origin_x, origin_y + tdy)].door.openess
                            if cx > P / dx:
                                # print(str(cx)+' > ' + str(P) + ' / ' + str(dx) + ' ... ' + str(cy))
                                if tdx == 1:
                                    texture_x = int((1 - (cx - P / dx)) * 64)
                                elif tdx == -1:
                                    texture_x = int((cx - P / dx) * 64)
                                else:
                                    texture_x = 32
                                # print(texture_x)
                                origin_y += tdy
                                break

                            else:
                                cx -= cy
                                cy = tick_y
                                origin_y += tdy
                        else:
                            cx -= cy
                            if tdx == 1:
                                texture_x = int((1 - (cx * dx)) * 64)
                            elif tdx == -1:
                                texture_x = int((cx * dx) * 64)
                            else:
                                texture_x = 32
                            origin_y += tdy
                            shading = True
                            break
                    else:
                        cx -= cy
                        cy = tick_y
                        origin_y += tdy

                elif cy > cx:
                    distance += cx
                    if self.gamemap[(origin_x + tdx, origin_y)].skin != None:
                        if self.gamemap[(origin_x + tdx, origin_y)].door and 0>1:
                            P = self.gamemap[(origin_x, origin_y + tdy)].door.openess
                            if cy > P / dy:
                                if tdy == 1:
                                    texture_x = int((1 - (cy - P / dy)) * 64)
                                elif tdy == -1:
                                    texture_x = int((cy - P / dy) * 64)
                                else:
                                    texture_x = 32
                                origin_x += tdx
                                break
                            else:
                                cy -= cx
                                cx = tick_x
                                origin_x += tdx

                        else:
                            cy -= cx
                            if tdy == 1:
                                texture_x = int((1 - (cy * dy)) * 64)
                            elif tdy == -1:
                                texture_x = int((cy * dy) * 64)
                            else:
                                texture_x = 32
                            origin_x += tdx
                            break
                    else:
                        cy -= cx
                        cx = tick_x
                        origin_x += tdx
                else:
                    cy += 0.000000000000001
                    # print("now that's rare")

            # if gamemap[(origin_x, origin_y)].door:
            #     distance = abs(int((distance * 64 + 24) * math.cos(math.radians(abs(-FOV/2 + ANGLE_SHIFT*(index))))-.5))
            # else:
            #     distance = abs(int(distance * 64 * math.cos(math.radians(abs(-FOV/2 + ANGLE_SHIFT*(index))))-.5))

            distance = abs(int(distance * 64 * cos(radians(abs(-FOV/2 + ANGLE_SHIFT*(index))))-.5))

            # Scale the distance to the grid unit, fix the fisheye
            # print(distance)
            # print(str(cx) +',' + str(dx))
            # if gamemap[(origin_x, origin_y)].skin == None:
            #     print((origin_x, origin_y))
            columns.append((distance, self.gamemap[(origin_x, origin_y)].skin, texture_x, shading))

            alpha += ANGLE_SHIFT
            if alpha > 360:
                alpha -= 360
        # print('stop')
        return columns

    def texture_slices(self, columns, sprites):
        x = 0

        for column in columns:
            try: # XXX This is crap, should check in the fix_distance
                height = int((64 / column[0] * PP_DISTANCE)+.5)
            except(ZeroDivisionError):
                height = int(64 * PP_DISTANCE+.5)

            if column[3] == True:
                sprites[x].color = Color(200,200,200,255)
            else:
                sprites[x].color = Color.WHITE

            sprites[x].set_texture_rect(IntRect(column[2]+64*column[1],0,1,64))
            sprites[x].position = (x, PP_HEIGHT/2 - height/2)
            sprites[x].scale = (1, height / 64)
            x += 1

        return sprites