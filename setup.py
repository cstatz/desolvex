# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from setuptools import setup, find_packages


dist = setup(setup_requires=['pbr>=1.9'], pbr=True)
