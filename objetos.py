#!/usr/bin/env python
#

import replika.assets
from replika.ingame import action

import glob
import random


class _ComportamientoMaletin(replika.ingame.Puppet):
    def __init__(self, *args, **kwargs):
        super(_ComportamientoMaletin, self).__init__(*args, **kwargs)
        self.current_action = self.initial

    @action
    def initial(self):
        self.current_action = self.move_down

    @action
    def move_down(self):
        if self.body.y > -300:
            self.body.y -= 15
        else:
            self.kill()

    def update(self):
        self.current_action()
        super(_ComportamientoMaletin, self).update()


def Maletin():
    _maletin = replika.assets.Puppet({
    'initial': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_0*.png')))),
    'final': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_broke_*.png'))),
        persistent=False),
    'move_down': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/maletin_0*.png'))))
    })
    _maletin.behaviour = _ComportamientoMaletin
    return _maletin
