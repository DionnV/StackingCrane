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
class Avg (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		self.page ('AVG')

		self.group ('Control', True)
		self.avgFront = Register(0)
		self.avgBack = Register(0)

		self.group ('Registers')
		self.avgFrontMoving = Register(0)
		self.avgFrontPos = Register(0)
		self.avgBackMoving = Register(0)
		self.avgBackPos = Register(0)

	def input(self, world):
		pass;

	def sweep(self):
		self.avgFrontMoving.set(0,self.avgFrontPos == self.avgFront,1)
		self.avgBackMoving.set(0,self.avgBackPos == self.avgBack,1)
		self.avgBackPos.set(self.avgBackPos - (self.avgBackPos-self.avgBack)*World.period,abs(self.avgBackPos._state-self.avgBack._state) > 0.01,self.avgBack)
		self.avgFrontPos.set(self.avgFrontPos - (self.avgFrontPos-self.avgFront)*World.period,abs(self.avgFrontPos._state-self.avgFront._state) > 0.01,self.avgFront)