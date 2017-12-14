__author__ = 'justinarmstrong'

import os
import pygame as pg
import constants as c
import time

keybinding = {
    'right':1,
    'jump':2,
    'still': 3,
    'action': 4,
    'down':5,
    'left':6,
}
keybinding_rev = {
    1: 'right',
    2: 'jump',
    3: 'still',
    4: 'action',
    5: 'down',
    6: 'left',
}

class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self, caption, redraw):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.action_start_time = 0.0
        self.current_action_idx = 0
        self.keys = keybinding['still']
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.redraw = redraw

        self.last_movement_time = 0.0
        self.last_position = -999

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.quit or self.state.game_info['mario dead']:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time, self.redraw)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist, self.redraw)
        self.state.previous = previous


    def event_loop(self, chromosome):

        if self.state_name == 'level1' and self.current_action_idx > 0:
            if self.last_position == self.state.viewport.x:
                if time.time()*1000.0 - self.last_movement_time > c.MAXIMAL_STILL_TIME:
                    print "Standing like an idiot for too long, terminate"
                    self.done = True
            else:
                # print "New best pos", self.state.viewport.x, "time ", self.current_time
                self.last_position = self.state.viewport.x
                self.last_movement_time = time.time()*1000.0

        if self.action_start_time == 0.0:
            self.action_start_time = time.time()*1000.0
            self.keys = chromosome[self.current_action_idx]
        elif time.time()*1000.0 - self.action_start_time > chromosome[self.current_action_idx+1]:
            self.current_action_idx += 2

            # print "Doing \"", keybinding_rev[chromosome[self.current_action_idx]], "\"\tfor time", chromosome[self.current_action_idx+1]
            if self.current_action_idx <= len(chromosome)-1:
                self.action_start_time = time.time()*1000.0
                self.keys = chromosome[self.current_action_idx]
            else:
                self.done = True


        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                # self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state.get_event(event)


    def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)


    def main(self, chromosome):
        """Main loop for entire program"""
        while not self.done:
            self.event_loop(chromosome)
            self.update()
            if self.redraw:
                pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)
        return self.state.viewport.x, self.current_action_idx

class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass



def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects











