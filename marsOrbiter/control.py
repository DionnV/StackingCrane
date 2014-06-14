from SimPyLC import *

class Control (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		self.thrusterForce = Register()
		
		self.mass = Register()
		self.velocity = Register()
		self.gravitationalConstant = Register()
		self.massMars = Register()
		self.orbitingDistance = Register()
		self.thrusterConstant = Register()
	
	def input (self, world):
		self.mass.set(world.marsOrbiter.mass)
		self.velocity.set(world.marsOrbiter.velocity)
		self.gravitationalConstant.set(world.marsOrbiter.gravitationalConstant)
		self.massMars.set(world.marsOrbiter.massMars)
		self.orbitingDistance.set(world.marsOrbiter.orbitingDistance)
		self.thrusterConstant.set(world.marsOrbiter.thrusterConstant)
	
	def sweep (self):
		self.thrusterForce.set(self.thrusterConstant * self.mass, self.velocity*self.velocity < self.gravitationalConstant * self.massMars/self.orbitingDistance, 0)
	
	def output (self, world):
		pass