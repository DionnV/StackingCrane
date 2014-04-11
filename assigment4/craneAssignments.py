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
class CraneAssignments (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)

		self.stage = Register(0);
		self.assignment = Register(1) # 1 for put,2 for get
		self.incrementStage = Register(0) # 1 for put,2 for get
		self.setX = Register(0) # from 0 to 30, containersizeunit :p
		self.setY = Register(0) # from 0 to 4, containersizeunit :p
		self.setZ = Register(0) # from 0 to 3, containersizeunit :p
		self.setSize = Register(30) # from 30 to 50
		self.go = Register(0)
		
		self.group('Output', True)
		self.X = Register(0)
		self.Y = Register(0)
		self.Z = Register(0)

		self.putX = Register(0)
		self.putY = Register(0)
		self.putZ = Register(0)

		self.SpreaderWidth = Register(30)
		self.spreaderPosition = Register(0)
		self.LockSpreader = Marker(0)
		
		#input

		self.group('Input')
		self.xPosition = Register(0) # from 0 to 30, containersizeunit :p
		self.yPosition = Register(0) # from 0 to 4, containersizeunit :p
		self.zPosition = Register(0) # from 0 to 3, containersizeunit :p
		self.spreaderSize = Register(0) # from 30 to 50


	def input (self, world):
		self.xPosition.set(world.crane.xPosition)
		self.yPosition.set(world.crane.yPosition)
		self.zPosition.set(world.crane.zPosition)
		self.spreaderPosition.set(world.crane.spreaderPosition)

	def sweep (self):
		self.X.set(0)
		self.Y.set(0)
		self.Z.set(0)
		
		self.stage.set(1,self.go == 1 and self.stage == 0)

		#get,stage = 1
		#go to z 3
		self.Z.set(1,self.stage == 1 and self.assignment == 2)
		self.incrementStage.set(1,self.zPosition > 2.9 and self.stage == 1 and self.assignment == 2)
		#go to sety,go to setx
		self.Y.set(max(-1,min(1,self.setY-self.yPosition)),self.stage == 2 and self.assignment == 2)
		self.X.set(max(-1,min(1,self.setX-self.xPosition)),self.stage == 2 and self.assignment == 2)
		self.incrementStage.set(1,self.yPosition > self.setY-0.01 and self.yPosition < self.setY+0.01 and self.xPosition > self.setX-0.01 and self.xPosition < self.setX+0.01 and self.stage == 2 and self.assignment == 2)
		#go to setZ, spreader setSize
		self.Z.set(max(-1,min(1,self.setZ-self.zPosition)),self.stage == 3 and self.assigment == 2)
		self.SpreaderWidth.set(self.setSize, self.stage == 3 and self.assigment == 2)
		self.incrementStage.set(1,self.zPosition > self.setZ-0.01 and self.zPosition < self.setZ+0.01 and self.spreaderPosition == self.SpreaderWidth and self.stage == 2 and self.assigment == 2)
		#speaderlock 1
		#go to z 3
		#go = 0

		#put,stage = 1
		#go to z 3
		self.Z.set(1, self.stage == 1 and self.assignment == 1)
		self.incrementStage.set(1, self.zPosition > 2.9 and self.stage == 1 and self.assignment == 1)
		
		#go to y 4
		self.Y.set(max(-1,min(1, 4 - self.yPosition._state)), self.stage == 2 and self.assignment == 1)
		self.incrementStage.set(1, self.yPosition > 3.9 and self.yPosition < 4.1 and self.stage == 2 and self.assignment == 1)
		
		#go to setX
		self.X.set(max(-1,min(1, self.setX - self.xPosition)), self.stage == 3 and self.assignment == 1)
		self.incrementStage.set(1, (self.setX > self.xPosition - 0.1 and self.setX < self.xPosition + 0.1) and self.stage == 3 and self.assignment == 1)
		
		#go to setY
		self.X.set(max(-1,min(1, self.setY - self.yPosition)), self.stage == 4 and self.assignment == 1)
		self.incrementStage.set(1, (self.setY > self.yPosition - 0.1 and self.setY < self.yPosition + 0.1) and self.stage == 4 and self.assignment == 1)
		
		#go to setZ
		self.X.set(max(-1,min(1, self.setZ - self.zPosition)), self.stage == 5 and self.assignment == 1)
		self.incrementStage.set(1, (self.setZ > self.zPosition - 0.1 and self.setZ < self.zPosition + 0.1) and self.stage == 5 and self.assignment == 1)
		
		#speaderlock 0
		self.LockSpreader.mark(0, self.stage == 6 and self.assignment == 1)
		self.incrementStage.set(1, self.LockSpreader == 0 and self.stage == 6 and self.assignment == 1)
		
		#go to z 3
		self.Z.set(1, self.stage == 7 and self.assignment == 1)
		self.incrementStage.set(1, self.zPosition > 2.9 and self.stage == 7 and self.assignment == 1)
		
		#go = 0
		self.go.set(0, self.stage == 8)


		self.putX.set(self.X)
		self.putY.set(self.Y)
		self.putZ.set(self.Z)
		self.stage.set(self.stage+1,self.incrementStage == 1)
		self.incrementStage.set(0)