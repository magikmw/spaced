#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Tile(object):
    """A basic tile class"""
    def __init__(self, position, blocked = True, skin = None, door = None):
        self.blocked = blocked
        self.skin = skin
        self.position = position

        self.door = door

    def add_door_component(self):
        if self.door:
            self.door.owner = self