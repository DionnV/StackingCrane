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
		self.xFriction = Register(0)
		self.xPosition = Register(0)
		self.xSpeed = Register(0)
		self.xMaxSpeed = Register(4)

		self.group ('Y')
		self.yMotor = Register(0)
		self.yFriction = Register(0)
		self.yPosition = Register(0)
		self.ySpeed = Register(0)
		self.yMaxSpeed = Register(2)

		self.group ('Z', True)
		self.zMotor = Register(0)
		self.zFriction = Register(0)
		self.zPosition = Register(0)
		self.zSpeed = Register(0)
		self.zMaxSpeed = Register(2)

		self.group ('Spreader')
		self.spreaderSet = Register(0)
		self.spreaderCanLock = Register(0)
		self.spreaderLockSet = Register(0)
		self.spreaderLock = Register(0)
		self.spreaderPosition = Register(30)
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
		self.updateEngine(self.xMotor,self.xPosition,self.xSpeed,self.xMaxSpeed,self.xFriction, 0 , 30)
		self.updateEngine(self.yMotor,self.yPosition,self.ySpeed,self.yMaxSpeed,self.yFriction, 0 , 4)
		self.updateEngine(self.zMotor,self.zPosition,self.zSpeed,self.zMaxSpeed,self.zFriction, 0 , 3)

		self.cableReelMoving.set(math.floor(self.xMotor._state),self.xMotor > 0,math.ceil(self.xMotor._state))
		self.endStopBack.set(1,self.xPosition > 29.95,0)
		self.endStopFront.set(1,self.xPosition < 0.04,0)
		
		self.spreaderPosition.set(self.spreaderSet)
		self.spreaderCanLock.set(1,self.yPosition > 0.95 and self.yPosition < 1.05 and (self.xPosition > 29.95 or self.xPosition < 0.05))
		self.spreaderLock.set(1,self.spreaderLockSet == 1 and self.spreaderCanLock == 1)
		self.spreaderLock.set(0,self.spreaderLockSet == 0)

	def updateEngine(self, motor, position , speed , maxspeed, friction, lowerbound, upperbound):
		friction.set(0.87,(motor < 0.1 and motor > -0.1),0.98)
		wantedspeed = ((motor*World.period*maxspeed) + speed)*friction*abs(self.emergencyBrake-1)
		speed.set(wantedspeed, wantedspeed < maxspeed)
		position.set(speed*World.period + position,((speed*World.period + position) < upperbound) and ((speed*World.period + position) > lowerbound),round(position._state))