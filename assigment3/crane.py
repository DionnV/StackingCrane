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
from math import *


class Crane(Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		self.page ('Cranephys')

		self.group ('X', True)
		self.xMotor = Register(0)
		self.xPosition = Register(0)
		self.xSpeed = Register(0)
		self.xMaxSpeed = Register(4)

		self.group ('Y')
		self.yMotor = Register(0)
		self.yPosition = Register(0)
		self.ySpeed = Register(0)
		self.yMaxSpeed = Register(4)

		self.group ('Z', True)
		self.zMotor = Register(0)
		self.zPosition = Register(0)
		self.zSpeed = Register(0)
		self.zMaxSpeed = Register(4)

		self.group ('Spreader')
		self.spreaderSet = Register(0)
		self.spreaderCanLock = Register(0)
		self.spreaderLockSet = Register(0)
		self.spreaderLock = Register(0)
		self.spreaderPosition = Register(0)
		self.spreaderMotor = Register(0)
		self.spreaderSpeed = Register(0)

		self.group ('Platform', True)
		self.platformFrontMoving = Register(0)
		self.platformBackMoving = Register(0)
		self.platformFrontAgv = Register(0)
		self.platformBackAgv = Register(0)

		self.group ('Other sensors')
		self.cableReelMoving = Register(0)
		self.endStopFront = Register(0)
		self.endStopBack = Register(0)

		self.group ('Other', True)
		self.emergencyBrake = Register(0)
		self.crash = Register(0)
		self.run = Runner(0)

	def input(self, world):
		self.xMotor.set(world.craneControl.xMotor)
		self.yMotor.set(world.craneControl.yMotor)
		self.zMotor.set(world.craneControl.zMotor)
		self.spreaderSet.set(world.craneControl.spreaderSet)
		self.spreaderLockSet.set(world.craneControl.spreaderLockSet)
		self.emergencyBrake.set(world.craneControl.emergencyBrake)

	def sweep(self):
		pass;