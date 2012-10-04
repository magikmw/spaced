#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main file for the game Spaced.

Should be called via a bash script in folder above"""

###
# DEVNOTES
###

# TODO - Write startup scripts and the SFML lib file switch for 32/64
# TODO - Implement logging
# TODO - Start on UI
# TODO - Make the doors slide [Jday requied]
# TODO - Wall-sliding (physics)
# TODO - Static enemies and items
# TODO - Shooting
# TODO - AI - Alien
# TODO - AI - Robot

###
# LOGGING
###

from log import logg

# ready to go!
# logging convention:
# logg.debug('') for variable passing
# logg.info('') for standard initialization messages
# logg.warn('') for known errors and caught exceptions
# logg.error('') for something that shouldn't happen
# logg.critical('') for breakage errors

logg.info('Logging initialized.')

###
# IMPORTS
###

logg.info('Start imports.')

# import sfml as sf
# logg.info('SFML imported')

from sfml import Clock, View, FloatRect, RenderWindow, VideoMode, Event, Texture, Color
logg.info('SFML imported')

from constants import PP_WIDTH, PP_HEIGHT, GAME_TITLE, GAME_VERSION, SCALE, BAR_HEIGHT
logg.info('Constants imported')

from gameworld import Gameworld

from drawable import text
logg.info('Drawable functions imported')

from raycaster import Raycaster
logg.info('Raycaster class imported')

from hud import Hud
logg.info('Hud class imported')

###
# DEBUG FUNCTIONS
##

clock = Clock()
frame = 0
fps = 0

def draw_fps(framein):
    global frame, fps

    frame += 1
    time = clock.elapsed_time.as_milliseconds()
    if time >= 1000:
        clock.restart()
        time = time/1000
        fps = int(framein/time)
        #logg.info('Frame: ' + str(frame) + '. FPS: ' + str(fps))
        frame = 0

    return fps

logg.info('Initializing the FPS counter')

###
# MAIN FUNCTION
###

def main():
    logg.info('Starting the main function')

    #Instancing, etc.

    main_view = View().from_rect(FloatRect(0,0,PP_WIDTH,PP_HEIGHT+BAR_HEIGHT))
    window = RenderWindow(VideoMode(PP_WIDTH*SCALE,PP_HEIGHT*SCALE), GAME_TITLE + ' v.' + GAME_VERSION)
    window.framerate_limit = 61
    window.view = main_view

    #Create an instance for all game variables and loop functions
    # and set the level to TESTLEVEL
    game = Gameworld()
    game.create_dict_map()
    game.player.gamemap = game.current_level

    # INITIALIZE TEXTURES HERE OR AFTER \o/
    TEXTURE_WALL = Texture.load_from_file('main/walls.png')
    TEXTURE_BAR = Texture.load_from_file('main/bar.png')
    TEXTURE_HUDWEAPONS = Texture.load_from_file('main/hud_weapons.png')
    TEXTURE_FACES = Texture.load_from_file('main/faces.png')

    #prepare the hud

    hud = Hud(player = game.player, background = TEXTURE_BAR, faces = TEXTURE_FACES, weapons = TEXTURE_HUDWEAPONS)

    #prepare the wall textures

    wall_sprites = game.create_wall_sprite_list(TEXTURE_WALL)

    rays = Raycaster(player = game.player, sprites = wall_sprites, gamemap = game.current_level)

    #prepare other stuff

    player_action = ''

    running = True
    nofocus = False

    ##
    #MAIN LOOP
    ##

    logg.info('Main loop starting...')
    while running:

        for event in window.iter_events():
            if event.type == Event.CLOSED or player_action == 'quit':
                running = False

            if event.type == Event.LOST_FOCUS:
                nofocus = True
            elif event.type == Event.GAINED_FOCUS:
                nofocus = False

        window.clear(Color(235,235,235,255))

        for sprite in wall_sprites:
            window.draw(sprite)

        window.draw(hud.background)
        window.draw(hud.face_full)
        window.draw(hud.pistol)

        debug_txt = text('['+str(draw_fps(frame))+'] ' + str(game.player.ux) + '(' + str(game.player.x) + '),'+str(game.player.uy) + '(' + str(game.player.y) + '):' + str(game.player.heading), style = 1)
        window.draw(debug_txt)

        wall_sprites = rays.texture_slices(rays.cast_rays(), wall_sprites)

        if len(game.doors) != 0:
            # print('lol doors')
            for door in game.doors:
                # print(door.openess)
                state =  door.open_close()
                # print(state)
                if state == 'done':
                    # print('removing doors')
                    game.doors.remove(door)

        if not nofocus:
            player_action = game.handle_keys()

        window.display()

    window.close()

if __name__ == '__main__':
    main()

else:
    logg.info['This file is not supposed to be imported.']
    print('This file is not supposed to be imported.')