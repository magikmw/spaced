#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Door(object):
    """Basic doors"""
    def __init__(self, player, openess = 0, timer = 180, incrament = 0.05, state = 0):
        self.openess = openess
        self.timer = timer
        self.incrament = incrament
        self.state = state
        self.player = player

    def open_close(self):
        if self.state == 1:
            if self.openess < 1:
                self.openess += self.incrament
                if self.openess > 1: self.openess = 1
            elif self.openess >= 1:
                self.owner.blocked = False
                self.timer -= 1
                # print((player.x, player.y) != self.owner.position)
                # print(self.owner.position)
                if self.timer <= 0 and (self.player.x, self.player.y) != self.owner.position:
                    self.owner.blocked = True
                    self.state = -1
        
        elif self.state == -1:
            self.openess -= self.incrament
            if self.openess <= 0:
                self.timer = 180
                self.state = 0
                self.openess = 0
                return 'done'