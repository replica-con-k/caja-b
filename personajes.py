#!/usr/bin/env python
#

import replika.assets
from replika.ingame import action

import glob

class _ComportamientoPolitico(replika.ingame.Puppet):
    def __init__(self, *args, **kwargs):
        super(_ComportamientoPolitico, self).__init__(*args, **kwargs)
        self.current_action = self.initial

    @action
    def initial(self):
        if self.current_animation.is_finished:
            self.stop()

    @action
    def move_left(self):
        if self.body.x > -480:
            self.body.x -= 10
        else:
            self.stop()

    @action
    def stand_left(self):
        pass
    
    @action
    def move_right(self):
        if self.body.x < 480:
            self.body.x += 10
        else:
            self.stop()

    @action
    def stand_right(self):
        pass
    
    def stop(self):
        if self.current_action == self.move_right:
            self.current_action = self.stand_right
        elif self.current_action == self.move_left:
            self.current_action = self.stand_left

    def update(self):
        self.current_action()
        super(_ComportamientoPolitico, self).update()


def Politico():
    _politico = replika.assets.Puppet({
    'initial': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/politico1_quieto_*.png')))),
    'move_right': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico1_corre_*.png')))),
    'stand_right': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico1_quieto_*.png')))),
    'move_left': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico1_corre_*.png')),
                              horizontal_flip=True)),
    'stand_left': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico1_quieto_*.png')),
                              horizontal_flip=True))
    })
    _politico.behaviour = _ComportamientoPolitico
    return _politico
