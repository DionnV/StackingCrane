from SimPyLC import *

class MarsOrbiter (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		
		self.phase = Register()
		self.thrusterForce = Register()
		self.gravityForce = Register()
		self.velocity = Register()
		self.distance = Register()
		
		self.mass = Register(1)
		self.massMars = Register(64185*10**19)
		self.massEarth = Register(59742*10**20)
	
		self.earthRadius = Register(6378*10**3)
		self.marsRadius = Register(3396*10**3)
	
		self.distanceToMars = Register(557*10**5)		
		self.orbitingDistance = Register(200*10**3)
		
		self.gravitationalConstant = Register(667*10**-13)	
		self.thrusterConstant = Register(1000)
		
		self.earthGravity = Register()
		self.marsGravity = Register()
		
		self.distanceLimit = Register()
		self.notCloseEnough = Marker()
		
		self.run = Runner()
		
	def input (self, world):		
		self.thrusterForce.set(world.control.thrusterForce)
		
	
	def sweep (self):
		self.phase.set(self.phase + 1, (self.distance >= 1000000 and self.phase == 0) or (self.distance >= 3000000 and self.phase == 1))
		self.earthGravity.set(self.gravitationalConstant * (self.mass * self.massEarth)/((self.earthRadius + self.distance)*(self.earthRadius + self.distance)))
		self.marsGravity.set(self.gravitationalConstant * (self.mass * self.massMars)/((self.distanceToMars - (self.earthRadius + self.distance))*(self.distanceToMars - (self.earthRadius + self.distance))))
		self.gravityForce.set(self.earthGravity + self.marsGravity)
				
		self.velocity.set(self.velocity + (((self.thrusterForce - self.gravityForce)/self.mass) * World.period), self.distance >= 0, 0)
		
		self.distanceLimit.set(self.distanceToMars - self.orbitingDistance)
		self.notCloseEnough.mark(self.distance < self.distanceLimit)
		self.distance.set(self.distance + (self.velocity * World.period), self.notCloseEnough, self.distance)
		
	
	def output(self, world):
		pass
		