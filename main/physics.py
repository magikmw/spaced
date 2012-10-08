#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from log import logg

logg.info('Physics initialized.')

import Box2D as b2
from math import radians

class Physics(object):
    """Class containing all the physics calculations."""

    def __init__(self, player, level, level_width, level_height):

        worldAABB = b2.b2AABB()

        worldAABB.upperBound = (.5, .5)
        worldAABB.lowerBound = (level_width, level_height)

        gravity = (0, 0)
        doSleep = True

        self.world = b2.b2World(gravity, doSleep)

        wall_shape = b2.b2PolygonShape()
        wall_shape.SetAsBox(.5, .5)
        wall_fixture = b2.b2FixtureDef()
        wall_fixture.shape = wall_shape
        wall_fixture.density = 5.0
        wall_fixture.friction = 0.5
        wall_fixture.reistitution = 0

        wall_body = b2.b2BodyDef()
        wall_body.type = b2.b2_staticBody
        wall_body.angle = 0
        wall_body.allowSleep = True
        wall_body.awake = False
        wall_body.fixedRotation = True
        wall_body.fixtures = [wall_fixture]

        for x in range(level_width):
            for y in range(level_height):
                if level[(x, y)].blocked:
                    wall_body.position = (x+0.5, y+.5)
                    level[(x, y)].body = self.world.CreateBody(wall_body)

        player_shape = b2.b2CircleShape()
        player_shape.radius = 0.3

        player_fixture = b2.b2FixtureDef()
        player_fixture.shape = player_shape
        player_fixture.density = 1
        player_fixture.friction = 0.5
        player_fixture.reistitution = 5

        player_body = b2.b2BodyDef()
        player_body.type = b2.b2_dynamicBody
        player_body.angle = radians(player.heading)
        player_body.position = (player.ux, player.uy)
        player_body.allowSleep = True
        player_body.awake = True
        player_body.fixtures = [player_fixture]
        player_body.linearDamping = 3.5

        player.body = self.world.CreateBody(player_body)