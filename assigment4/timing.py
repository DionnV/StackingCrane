# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

from SimPyLC import *


class Timing(Chart):
    def __init__(self, name):
        Chart.__init__(self, name)

    def define(self, world):

        self.channel(world.crane.xPosition, blue, 0, 30, 50)
        self.channel(world.crane.yPosition, yellow, 0, 4, 50)
        self.channel(world.crane.zPosition, aqua, 0, 3, 50)
        self.channel(world.crane.spreaderPosition, teal, 30, 50, 50)

        #blue,lime,yellow,silver,aqua,purple,navy,teal,fuchsia,maroon