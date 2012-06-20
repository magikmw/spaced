#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sfml import RectangleShape, Text, Color

def line(size=(1,1), outline_color = Color.BLACK, x=0, y=0, rotate = 0, outline_thickness = 1):
    l = RectangleShape()
    l.size = size
    l.outline_color = outline_color
    l.outline_thickness = outline_thickness
    l.x = x
    l.y = y
    if rotate != 0:
        l.rotate(rotate)

    return l

def dot(x, y, size=(1,1), outline_color = Color.RED, outline_thickness = 1):
    d = RectangleShape()
    d.size = size
    d.outline_color = outline_color
    d.outline_thickness = outline_thickness
    d.x = x
    d.y = y

    return d

def text(string, character_size = 12, color = Color.BLACK, style = 0):
    t = Text(string)
    t.character_size = character_size
    t.color = color
    t.style = style

    return t