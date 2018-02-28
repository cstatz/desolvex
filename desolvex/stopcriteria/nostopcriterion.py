# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'


class NoStopCriterion(object):

    def __init__(self):

        self.__maximum_iterations = 1
        self.__variables_dict = dict()
        self.__variables_dict['iteration'] = 0

    @property
    def int_maximum(self):
        return self.__maximum_iterations

    @property
    def int_value(self):
        return self.__variables_dict['iteration']

    def met(self):

        if self.__variables_dict['iteration'] < self.__maximum_iterations:
            return False

        return True

    def update(self):
        pass

