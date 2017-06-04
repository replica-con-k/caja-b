#!/usr/bin/env python
#

import replika.assets
from replika.ingame import action

import personajes

import glob
import random

GRAVITY=-1

class _ComportamientoMaletin(replika.ingame.Puppet):
    def __init__(self, *args, **kwargs):
        super(_ComportamientoMaletin, self).__init__(*args, **kwargs)
        self.current_action = self.initial
        self.speed = (0, 0)

    @action
    def initial(self):
        if self.speed[0] != 0:
            self.current_action = self.fall_down
        else:
            self.current_action = self.move_down

    @action
    def move_down(self):
        if self.body.y > -290:
            self.body.y += self.speed[1]
        else:
            self.speed = (0, 0)
            self.current_action = self.lost

    @action
    def fall_down(self):
        self.body.x += self.speed[0]
        if self.body.y > -280:
            self.body.y += self.speed[1]
        else:
            self.speed = (0, 0)
            self.current_action = self.lost

    @action
    def lost(self):
        if self.current_animation.is_finished:
            self.kill()

    @action
    def stolen(self):
        if self.current_animation.is_finished:
            self.kill()
            
    def update(self):
        self.current_action()
        self.speed = (self.speed[0], self.speed[1] + GRAVITY)
        super(_ComportamientoMaletin, self).update()

    def collision(self, element):
        if not isinstance(element, personajes._ComportamientoPolitico):
            return
        if self.current_action in [self.stolen, self.lost]:
            return
        element.score += 10
        self.current_action = self.stolen


def Maletin():
    _maletin = replika.assets.Puppet({
    'initial': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_0*.png')))),
    'lost': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_broke_*.png'))),
        persistent=False),
    'move_down': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_0*.png')))),
    'fall_down': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_parabola_0*.png')))),
    'stolen': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_cogido_0*.png'))))
    })
    _maletin.behaviour = _ComportamientoMaletin
    return _maletin

def cuerpo_maletin():
    return replika.physics.create_body(
        replika.assets.image('assets/maletin_0001.png')
    )
