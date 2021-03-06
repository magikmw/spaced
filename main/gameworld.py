#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Gameworld initialized.')

import math

from tile import Tile

from door import Door

from player import Player

from weapons import Weapons

from physics import Physics

from entity import Entity

from constants import PLAYER_SPEED, TURN_SPEED, PP_HEIGHT, PP_WIDTH, HEAD_BOB

# from __main__ import TEXTURE_ENEMIES

from sfml import Keyboard, IntRect, Sprite, Event

TESTLEVEL = [   ['#', ']', '[', '=', ']', '#', '#', '#', '#', '#', '#'],
                [']', '.', '.', '.', '.', '#', '.', '.', '$', '.', '#'],
                ['#', '.', '$', '.', '.', '$', '.', '.', '$', '.', '#'],
                ['#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
                ['#', '.', '$', '.', '.', '%', '.', '.', '$', '.', '#'],
                ['#', '.', '.', '.', '.', '#', '.', '.', '$', '.', '#'],
                ['#', '.', '.', '.', '.', '$', '.', '.', '.', '.', '#'],
                ['#', '%', '#', '#', '#', '#', '#', '%', '#', '#', '#'],
                ['#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
                ['$', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
                ['$', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
                ['$', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
                ['$', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
                ['#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
                ['#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#'],
                ['#', '[', '=', '=', ']', '$', '#', '#', '#', '#', '#']]

TESTLEVEL_WIDTH = 16
TESTLEVEL_HEIGHT = 11

class Gameworld(object):
    def __init__(self, texture_enemies):
        self.doors = []
        self.current_level = None
        self.rifle = Weapons(ident = 'rifle', ammo = 50, enabled = 1)
        self.pistol = Weapons(ident = 'pistol', ammo = 10, enabled = 1)
        self.knife = Weapons(ident = 'knife', ammo = 0, enabled = 1)
        self.player = Player(gamemap = self.current_level, weapon = self.knife)
        
        if HEAD_BOB == True:
            self.bob_top = True
        else:
            self.bob_top = 'no bobbing'

        self.entities = []
        #8-14 x, 6-9 y
        for x in range(10,11):
            for y in range(7,8):
                test = Entity(x, y, texture_enemies, 0, 0)
                self.entities.append(test)

    def create_dict_map(self, width = TESTLEVEL_WIDTH, height = TESTLEVEL_HEIGHT, level_array = TESTLEVEL):
        dict_map = {(x,y):Tile((x,y)) for x in range(width) for y in range(height)} 


        for l_x in range(width):
            for l_y in range(height):
                if level_array[l_x][l_y] == '.':
                    dict_map[(l_x, l_y)].blocked = False
                elif level_array[l_x][l_y] == '#':
                    dict_map[(l_x, l_y)].skin = 0
                elif level_array[l_x][l_y] == '$':
                    dict_map[(l_x, l_y)].skin = 1
                elif level_array[l_x][l_y] == '%':
                    dict_map[(l_x, l_y)].skin = 2
                    door_component = Door(player = self.player, entities = self.entities)
                    dict_map[(l_x, l_y)].door = door_component
                    dict_map[(l_x, l_y)].add_door_component()
                elif level_array[l_x][l_y] == '[':
                    dict_map[(l_x, l_y)].skin = 3
                elif level_array[l_x][l_y] == '=':
                    dict_map[(l_x, l_y)].skin = 4
                elif level_array[l_x][l_y] == ']':
                    dict_map[(l_x, l_y)].skin = 5

        self.current_level = dict_map

    def open_doors(self):

        dirx = math.cos(math.radians(self.player.heading))
        diry = math.sin(math.radians(self.player.heading))

        new_x = int(self.player.ux + -dirx*1)
        new_y = int(self.player.uy + -diry*1)

        if self.current_level[(new_x, new_y)].door and not self.current_level[(new_x, new_y)].door in(self.doors):
            self.current_level[(new_x, new_y)].door.state = 1
            self.doors.append(self.current_level[(new_x, new_y)].door)

        else:
            pass # TODO - sound of 'nope' from Half-Life \o/

    def handle_keys(self):
        """Simple key handling. Does not return values, except for the ESC key!"""

        if Keyboard.is_key_pressed(Keyboard.ESCAPE):
            return 'quit'

        if Keyboard.is_key_pressed(Keyboard.E):
            self.player.turn(TURN_SPEED)
        elif Keyboard.is_key_pressed(Keyboard.Q):
            self.player.turn(-TURN_SPEED)

        if Keyboard.is_key_pressed(Keyboard.A):
            self.player.strafing = True
            self.player.strafe(PLAYER_SPEED, "left")

        elif Keyboard.is_key_pressed(Keyboard.D):
            self.player.strafing = True
            self.player.strafe(PLAYER_SPEED, "right")           

        if Keyboard.is_key_pressed(Keyboard.W):
            self.player.move(PLAYER_SPEED, "forward")
            if self.bob_top == True:
                if self.player.bob < 5:
                    self.player.bob += .5
                else:
                    self.bob_top = False
            elif self.bob_top == False:
                if self.player.bob > -5:
                    self.player.bob -= .5
                else:
                    self.bob_top = True

        elif Keyboard.is_key_pressed(Keyboard.S):
            self.player.move(PLAYER_SPEED, "backward")
            if self.bob_top == True:
                if self.player.bob < 5:
                    self.player.bob += .5
                else:
                    self.bob_top = False
            elif self.bob_top == False:
                if self.player.bob > -5:
                    self.player.bob -= .5
                else:
                    self.bob_top = True            

        if Keyboard.is_key_pressed(Keyboard.SPACE):
            self.open_doors()

        if Keyboard.is_key_pressed(Keyboard.R_CONTROL) and self.player.attack_delay == 0 and self.player.attack == False:
            self.player.attack = True
            self.player.attack_delay = 15

        if Keyboard.is_key_pressed(Keyboard.NUM1) and self.knife.enabled == 1:
            self.player.weapon = self.knife
        elif Keyboard.is_key_pressed(Keyboard.NUM2) and self.pistol.enabled == 1:
            self.player.weapon = self.pistol
        elif Keyboard.is_key_pressed(Keyboard.NUM3) and self.rifle.enabled == 1:
            self.player.weapon = self.rifle

        # DEBUG KEYS
        if Keyboard.is_key_pressed(Keyboard.P):
            if self.player.hp + 5 <= 100:
                self.player.hp += 5
        elif Keyboard.is_key_pressed(Keyboard.O):
            if self.player.hp - 5 >= 0:
                self.player.hp -= 5

        if Keyboard.is_key_pressed(Keyboard.R_BRACKET):
            if self.player.score + 55 < 9999:
                self.player.score += 55
        elif Keyboard.is_key_pressed(Keyboard.L_BRACKET):
            if self.player.score - 55 >= 0:
                self.player.score -= 55

    def create_wall_sprite_list(self, texture):
        sprite = Sprite(texture)
        wall_sprites = []
        for i in range(PP_WIDTH):
            wall_sprite = sprite.copy()
            wall_sprite.position = (i, PP_HEIGHT/2 - 32)
            wall_sprite.set_texture_rect(IntRect(0,0,1,64))
            wall_sprites.append(wall_sprite)

        return wall_sprites

    def init_physics(self):
        self.physics = Physics(player = self.player, level = self.current_level, level_width = TESTLEVEL_WIDTH, level_height = TESTLEVEL_HEIGHT)