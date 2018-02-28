# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

import numpy as np

from maui import context
from maui.field import ScalarField
from maui.mesh import CartesianMesh
from copy import deepcopy

from .domain import Domain


class CartesianDomain(Domain):

    def __init__(self, bounds, pitch, fields, variables, coordinates=('x', 'y', 'z'), initializer=None):

        # initialize meshes/discretization
        # initialize partitions too!
        meshes = dict()

        # TODO: this is not yet completely correct!
        meshes['node'] = CartesianMesh((bounds[0],tuple(np.asarray(bounds[1]) - pitch)), pitch)
        partition = context.create_partition(CartesianMesh((bounds[0],tuple(np.asarray(bounds[1]) - pitch)), pitch))

        if 'cell' in fields.keys():
            meshes['cell'] = meshes['node'].copy().shift(tuple([pitch/2. for _ in coordinates]))

        if 'edge' in fields.keys():
            meshes['edge'] = dict()
            for i, axis in enumerate(coordinates):
                # TODO: Modify size! create base mesh, modify size.
                offset = [0 for _ in coordinates]
                offset[i] = pitch/2.
                meshes['edge'][axis] = meshes['node'].copy().shift(tuple(offset))

        if 'face' in fields.keys():
            meshes['face'] = dict()
            for i, axis in enumerate(coordinates):
                # TODO: Modify size! create base mesh, modify size.
                offset = [False for _ in coordinates]
                offset[i] = True
                offset[:] = [not i for i in offset]
                offset[:] = [pitch/2.*i for i in offset]
                meshes['face'][axis] = meshes['node'].copy().shift(tuple(offset))

        # The node meshes are always +1 cell bigger in each direction than all other meshes! 
        # TODO: This is a crude hack that doesn't work with multiple subdomains (i.e. MPI)!
    	# This can only be fixed, if the mesh is extended in the last domains according to the partition.
        # Modify node partition (iterate over partition and replace submeshes to enlarge!)
        partition.mesh = CartesianMesh(bounds, pitch)

        for domain in partition.domains:
            high = list()

            for h in partition.domains[domain].mesh.bounds[1]:
                high.append(h + pitch)

            partition.domains[domain].mesh = CartesianMesh((partition.domains[domain].mesh.bounds[0], tuple(high)), pitch)

        meshes['node_wrap'] = partition
        
        Domain.__init__(self, meshes, fields, variables, coordinates, initializer)
