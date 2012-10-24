#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main file for the game Spaced.

Should be called via a bash script in folder above"""

###
# DEVNOTES
###

# TODO - Screenshot key
# TODO - Write log clear // win build file
# TODO - Implement logging
# TODO - Make the doors slide [Jday requied]
# TODO - Items
# TODO - Shooting
# TODO - Optimize HUD.prepare()
# TODO - Enemy sides - sprites
# TODO - Audio

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
average_fps = 0
all_frames = 0

def draw_fps(framein):
    global frame, fps, all_frames, average_fps

    frame += 1
    time = clock.elapsed_time.as_milliseconds()
    if time >= 1000:
        clock.restart()
        time = time/1000
        fps = int(framein/time)+1
        # logg.info('FPS: ' + str(fps))
        frame = 0

    average_fps += fps
    all_frames += 1

    return fps

logg.info('Initializing the FPS counter')

###
# MAIN FUNCTION
###

def main():
    logg.info('Starting the main function')

    #Instancing, etc.

    main_view = View().from_rect(FloatRect(0,0,PP_WIDTH,PP_HEIGHT+BAR_HEIGHT))
    window = RenderWindow(VideoMode(PP_WIDTH*SCALE,(PP_HEIGHT+BAR_HEIGHT)*SCALE), GAME_TITLE + ' v.' + GAME_VERSION)
    window.framerate_limit = 61
    window.view = main_view

    # INITIALIZE TEXTURES HERE OR AFTER \o/
    TEXTURE_WALL = Texture.load_from_file('main/walls.png')
    TEXTURE_BAR = Texture.load_from_file('main/bar.png')
    TEXTURE_HUDWEAPONS = Texture.load_from_file('main/hud_weapons.png')
    TEXTURE_FACES = Texture.load_from_file('main/faces.png')
    TEXTURE_NUMBERS = Texture.load_from_file('main/numbers.png')
    TEXTURE_WEAPONS = Texture.load_from_file('main/weapons.png')
    TEXTURE_ENEMIES = Texture.load_from_file('main/test.png')

    #Create an instance for all game variables and loop functions
    # and set the level to TESTLEVEL
    game = Gameworld(TEXTURE_ENEMIES)
    game.create_dict_map()
    game.player.gamemap = game.current_level
    game.init_physics()
    game.physics.mob_bodies(game.entities)

    #prepare the hud

    hud = Hud(player = game.player, background = TEXTURE_BAR, faces = TEXTURE_FACES, hudweapons = TEXTURE_HUDWEAPONS, weapons = TEXTURE_WEAPONS, numbers = TEXTURE_NUMBERS)

    #prepare the wall textures

    wall_sprites = game.create_wall_sprite_list(TEXTURE_WALL)

    rays = Raycaster(player = game.player, sprites = wall_sprites, gamemap = game.current_level)

    #prepare other stuff

    player_action = ''

    running = True
    nofocus = False

    ##
    # MAIN LOOP
    ##

    logg.info('Main loop starting...')
    while running:

        #iterate events

        for event in window.iter_events():
            if event.type == Event.CLOSED or player_action == 'quit':
                running = False

            if event.type == Event.LOST_FOCUS:
                nofocus = True
            elif event.type == Event.GAINED_FOCUS:
                nofocus = False

            if event.type == Event.KEY_RELEASED:
                if game.player.bob > 0:     #level the headbobbing
                    game.player.bob -= .5
                elif game.player.bob < 0:
                    game.player.bob += .5

                game.player.strafing = False 
                    #disable speed limiter for moving in 2 axii

        window.clear(Color(235,235,235,255)) #clear the window of everything

        for sprite in wall_sprites: #draw walls
            window.draw(sprite)

        #draw entities here
        for entity in game.entities:
            if entity.visible == True:
                for sprite_slice in entity.sprite:
                    window.draw(sprite_slice)

        hud.display(window) #draw the hud

        debug_txt = text('['+str(draw_fps(frame))+'] ' + str("{0:.2f}".format(game.player.ux)) + '(' + str(game.player.x) + '),'+str("{0:.2f}".format(game.player.uy)) + '(' + str(game.player.y) + '):' + str(game.player.heading), style = 1)
        window.draw(debug_txt)

        wall_sprites = rays.texture_slices(rays.cast_rays(), wall_sprites, game.player.bob) #determine which walls to display

        #determine wich entities to display and prepare
        for entity in game.entities: #calculate the distance of entities to the player
            entity.distance_to_player(game.player)
            # print(str(round(entity.distance, 2)) + " " + str(entity.x) + "," + str(entity.y))

        game.entities.sort(key=lambda x: x.distance, reverse=True) #sort entities based on the distance

        for entity in game.entities:
            entity.set_sprite_for_display(game.player, rays.distances)


        ###
        # TIMERS
        ###

        if game.player.attack_delay > 0 and game.player.attack == True:
            game.player.attack_delay -= 1
        elif game.player.attack == True and game.player.attack_delay == 0:
            game.player.attack = False
            game.player.attack_delay = 2
        elif game.player.attack == False and game.player.attack_delay > 0:
            game.player.attack_delay -= 1

        if len(game.doors) != 0:
            # print('lol doors')
            for door in game.doors:
                # print(door.openess)
                state =  door.open_close()
                # print(state)
                if state == 'done':
                    # print('removing doors')
                    game.doors.remove(door)

        game.physics.world.ClearForces()

        if not nofocus:
            player_action = game.handle_keys() #player input

        game.physics.world.Step(1.0/60.0, 10, 8)

        game.player.update_position()
        for entity in game.entities:
            entity.update_position()

        window.display() #blit to window

    window.close()

    logg.info('Terminating. Have a nice day.')
    logg.info('Average FPS: %s', round(average_fps/all_frames, 2))

if __name__ == '__main__':
    main()

else:
    logg.info('This file is not supposed to be imported.')
    print('This file is not supposed to be imported.')