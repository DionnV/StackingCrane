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
class CraneControl (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		self.run = Runner();

		#input
		self.xPosition = Register(0) # from 0 to 30, containersizeunit :p
		self.yPosition = Register(0) # from 0 to 4, containersizeunit :p
		self.zPosition = Register(0) # from 0 to 3, containersizeunit :p

		self.spreaderCanLock = Register(0) # 1 or 0
		self.spreaderPosition = Register(0) # 30 to 50

		self.platformFrontMoving = Register(0) # 1 or 0
		self.platformBackMoving = Register(0) # 1 or 0
		self.platformFrontAgv = Register(0) # 1 or 0
		self.platformBackAgv = Register(0) # 1 or 0

		self.cableReelMoving = Register(0) # 1,0,-1
		self.endStopFront = Register(0) # 1 or 0
		self.endStopBack = Register(0) # 1 or 0


		#output
		self.xMotor = Register(0) # from -1 to 1
		self.yMotor = Register(0) # from -1 to 1
		self.zMotor = Register(0) # from -1 to 1
		self.spreaderSet = Register(0) # 30,40,50
		self.spreaderLockSet = Register(0) # 1 or 0
		self.emergencyBrake = Register(0) # 1 or 0

		
	def input (self, world):
		self.xPosition.set(world.craneControl.xPosition)
		self.yPosition.set(world.craneControl.yPosition)
		self.zPosition.set(world.craneControl.zPosition)

		self.spreaderCanLock.set(world.craneControl.spreaderCanLock)
		self.spreaderPosition.set(world.craneControl.spreaderPosition)

		self.platformFrontMoving.set(world.craneControl.platformFrontMoving)
		self.platformBackMoving.set(world.craneControl.platformBackMoving)
		self.platformFrontAgv.set(world.craneControl.platformFrontAgv)
		self.platformBackAgv.set(world.craneControl.platformBackAgv)

		self.cableReelMoving.set(world.craneControl.cableReelMoving)
		self.endStopFront.set(world.craneControl.endStopFront)
		self.endStopBack.set(world.craneControl.endStopBack)
	
	def sweep (self):
		pass;
		