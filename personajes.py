#!/usr/bin/env python
#

import replika.assets
from replika.ingame import action

import glob
import random

import objetos

class _ComportamientoPolitico(replika.ingame.Puppet):
    def __init__(self, *args, **kwargs):
        super(_ComportamientoPolitico, self).__init__(*args, **kwargs)
        self.current_action = self.initial
        self.score = 0

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


def Politico(n=1):
    _politico = replika.assets.Puppet({
    'initial': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/politico%s_quieto_*.png' % n)))),
    'move_right': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico%s_corre_*.png' % n)))),
    'stand_right': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico%s_quieto_*.png' % n)))),
    'move_left': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico%s_corre_*.png' % n)),
            horizontal_flip=True)),
    'stand_left': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/politico%s_quieto_*.png' % n)),
            horizontal_flip=True))
    })
    _politico.behaviour = _ComportamientoPolitico
    return _politico

def cuerpo_politico(n):
    return (replika.physics.create_body(
        replika.assets.image('assets/politico1_quieto_01.png')) if n == 1 else
            replika.physics.create_body(
                replika.assets.image('assets/politico2_quieto_0001.png'))
    )

class _ComportamientoCorrupto(replika.ingame.Puppet):
    def __init__(self, *args, **kwargs):
        super(_ComportamientoCorrupto, self).__init__(*args, **kwargs)
        self.current_action = self.initial
        self._throw_delay_ = 5

    @action
    def initial(self):
        if self.current_animation.is_finished:
            self.current_action = self.move_right

    def _throw_money_(self):
        if random.randint(0, 10) == 5:
            return True
        return False
    
    @action
    def move_left(self):
        if self.body.x > -390:
            self.body.x -= 8
            if self._throw_money_():
                self._throw_delay_ = 5
                self.current_action = random.choice([self.drop_left,
                                                     self.throw_left])
        else:
            self.current_action = self.move_right

    @action
    def move_right(self):
        if self.body.x < 390:
            self.body.x += 8
            if self._throw_money_():
                self._throw_delay_ = 5
                self.current_action = random.choice([self.drop_right,
                                                     self.throw_right])
        else:
            self.current_action = self.move_left

    @action
    def drop_left(self):
        self._throw_delay_ -= 1
        if self._throw_delay_ == 0:
            maletin = self.layer.add_asset(
                objetos.Maletin(),
                position=(self.body.x - 50, self.body.y))
            maletin.speed = (0, 0)
            maletin.body = objetos.cuerpo_maletin()
        if self.current_animation.is_finished:
            self.current_action = self.move_left

    @action
    def drop_right(self):
        self._throw_delay_ -= 1
        if self._throw_delay_ == 0:
            maletin = self.layer.add_asset(
                objetos.Maletin(),
                position=(self.body.x + 50, self.body.y))
            maletin.speed = (0, 0)
            maletin.body = objetos.cuerpo_maletin()
        if self.current_animation.is_finished:
            self.current_action = self.move_right

    @action
    def throw_left(self):
        self._throw_delay_ -= 1
        if self._throw_delay_ == 0:
            maletin = self.layer.add_asset(
                objetos.Maletin(),
                position=(self.body.x - 50, self.body.y))
            maletin.speed = (-5, 5)
            maletin.body = objetos.cuerpo_maletin()
        if self.current_animation.is_finished:
            self.current_action = self.move_left

    @action
    def throw_right(self):
        self._throw_delay_ -= 1
        if self._throw_delay_ == 0:
            maletin = self.layer.add_asset(
                objetos.Maletin(),
                position=(self.body.x + 50, self.body.y))
            maletin.speed = (5, 5)
            maletin.body = objetos.cuerpo_maletin()
        if self.current_animation.is_finished:
            self.current_action = self.move_right

    def update(self):
        self.current_action()
        super(_ComportamientoCorrupto, self).update()


def Corrupto():
    _corrupto = replika.assets.Puppet({
    'initial': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_anda_*.png')),
            horizontal_flip=True)),
    'move_right': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_anda_*.png')),
            horizontal_flip=True)),
    'move_left': replika.assets.Loop(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_anda_*.png')))),
    'drop_right': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_suelta_*.png')),
            horizontal_flip=True)),
    'drop_left': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_suelta_*.png')))),
    'throw_right': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_lanza_*.png')),
            horizontal_flip=True)),
    'throw_left': replika.assets.Animation(
        replika.assets.images(
            sorted(glob.glob('assets/corrupto_arriba_lanza_*.png'))))
    })
    _corrupto.behaviour = _ComportamientoCorrupto
    return _corrupto
