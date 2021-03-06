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
		#self.run = Runner();

		self.page('controls')
		
		self.group('Movement', True)
		self.X = Register(0)
		self.Y = Register(0)
		self.Z = Register(0)
		self.Emergency = Marker(0)
		self.Failure = Marker(0)
		self.SpreaderWidth = Register(30)
		self.LockSpreader = Marker(0)

		self.group('error')
		self.SpeaderSizeError = Register(0)

		self.group("input", True)
		
		#input
		self.xPosition = Register(0) # from 0 to 30, containersizeunit :p
		self.yPosition = Register(0) # from 0 to 4, containersizeunit :p
		self.zPosition = Register(0) # from 0 to 3, containersizeunit :p

		self.xVelocity = Register(0)

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
		self.X.set(world.craneAssignments.putX)
		self.Y.set(world.craneAssignments.putY)
		self.Z.set(world.craneAssignments.putZ)
		self.SpreaderWidth.set(world.craneAssignments.SpreaderWidth)
		self.LockSpreader.mark(world.craneAssignments.LockSpreader)

		self.xPosition.set(world.crane.xPosition)
		self.yPosition.set(world.crane.yPosition)
		self.zPosition.set(world.crane.zPosition)

		self.spreaderCanLock.set(world.crane.spreaderCanLock)
		self.spreaderPosition.set(world.crane.spreaderPosition)

		self.platformFrontMoving.set(world.crane.platformFrontMoving)
		self.platformBackMoving.set(world.crane.platformBackMoving)
		self.platformFrontAgv.set(world.crane.platformFrontAgv)
		self.platformBackAgv.set(world.crane.platformBackAgv)

		self.cableReelMoving.set(world.crane.cableReelMoving)
		self.endStopFront.set(world.crane.endStopFront)
		self.endStopBack.set(world.crane.endStopBack)

		self.xVelocity.set(world.crane.xSpeed)
	
	def sweep (self):
		self.moveX();
		self.moveY();
		self.moveZ();
		self.emergBrake();
		self.failureBrake();
		self.lockTwistlocks();	
		self.setSpreaderSize();


	def moveX(self):
		self.xMotor.set(self.X._state, self.X > 0 and self.X <= 1)
		self.xMotor.set(0, self.X == 0)
		self.xMotor.set(self.X._state, self.X < 0  and self.X >= -1)

		# check if cablereel is turning 
		self.xMotor.set(0, self.xVelocity > 0.1 and self.cableReelMoving == 0)

		# Only move if spreader is at the top
		self.xMotor.set(0, self.zPosition < 2.9)
		self.X.set(0, self.zPosition < 2.9)

		# Do not move when something else is moving and crane is near
		self.xMotor.set(0, (self.platformBackMoving == 1 and self.xPosition > 28.5) or (self.platformFrontMoving == 1 and self.xPosition < 1.5))
		self.X.set(0, (self.platformBackMoving == 1 and self.xPosition > 28.5) or (self.platformFrontMoving == 1 and self.xPosition < 1.5))

		# Endstops
		self.xMotor.set(0, self.endStopBack == 1 and self.X == 1)
		self.X.set(0, self.endStopBack == 1 and self.X == 1)
		self.xMotor.set(0, self.endStopFront == 1 and self.X == -1)
		self.X.set(0, self.endStopFront == 1 and self.X == -1)		

	def moveY(self):
		self.yMotor.set(self.Y._state, self.Y > 0  and self.Y >= -1)
		self.yMotor.set(0, self.Y == 0)
		self.yMotor.set(self.Y._state, self.Y < 0  and self.Y >= -1)

		# Only move if spreader is at the top
		self.yMotor.set(0, self.zPosition < 2.9)
		self.Y.set(0, self.zPosition < 2.9)

		# Do not move when something else is moving
		self.yMotor.set(0, (self.platformBackMoving == 1 and self.xPosition > 28.5) or (self.platformFrontMoving == 1 and self.xPosition < 1.5))
		self.Y.set(0, (self.platformBackMoving == 1 and self.xPosition > 28.5) or (self.platformFrontMoving == 1 and self.xPosition < 1.5))

		self.yMotor.set(0, self.yPosition > 3.95 and self.Y == 1)
		self.Y.set(0, self.yPosition > 3.95 and self.Y == 1)
		self.yMotor.set(0, self.yPosition < 0.05 and self.Y == -1)
		self.Y.set(0, self.yPosition < 0.05 and self.Y == -1)


	def moveZ(self):
		self.zMotor.set(self.Z._state, self.Z > 0  and self.Z <= 1)
		self.zMotor.set(0, self.Z == 0)
		self.zMotor.set(self.Z._state, self.Z < 0  and self.Z >= -1)

		# Do not move when something else is moving
		self.zMotor.set(0, (self.platformBackMoving == 1 and self.xPosition > 28.5) or (self.platformFrontMoving == 1 and self.xPosition < 1.5))
		self.Z.set(0, (self.platformBackMoving == 1 and self.xPosition > 28.5) or (self.platformFrontMoving == 1 and self.xPosition < 1.5))

		self.SpeaderSizeError.set(1,self.zPosition < 1 and self.spreaderCanLock == 0,0)

		self.zMotor.set(0, self.zPosition > 2.95 and self.Z == 1)
		self.Z.set(0, self.zPosition > 2.95 and self.Z == 1)
		self.zMotor.set(0, self.zPosition < 0.05 and self.Z == -1)
		self.Z.set(0, self.zPosition < 0.05 and self.Z == -1)

	def emergBrake(self):
		self.emergencyBrake.set(1, self.Emergency, 0)
		# stop motors only way to stop crane is to stop the motor
		self.xMotor.set(0, self.emergencyBrake)
		self.yMotor.set(0, self.emergencyBrake)
		self.zMotor.set(0, self.emergencyBrake)


	def failureBrake(self):
		self.emergencyBrake.set(1, self.Failure and self.xVelocity < 0.5 , 0)
		# stop motors only way to stop crane is to stop the motor
		self.xMotor.set(0, self.Failure or self.emergencyBrake)
		self.yMotor.set(0, self.Failure or self.emergencyBrake)
		self.zMotor.set(0, self.Failure or self.emergencyBrake)

	def lockTwistlocks(self):
		self.spreaderLockSet.set(1, self.spreaderCanLock == 1 and self.LockSpreader, 0)
		self.LockSpreader.mark(1, self.spreaderLockSet, 0)

	def setSpreaderSize(self):
		self.spreaderSet.set(30, self.SpreaderWidth == 30)
		self.spreaderSet.set(40, self.SpreaderWidth == 40)
		self.spreaderSet.set(50, self.SpreaderWidth == 50)