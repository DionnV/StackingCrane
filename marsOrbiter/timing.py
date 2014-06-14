from SimPyLC import *

class Timing (Chart):
	def __init__ (self, name):
		Chart.__init__ (self, name)
		
	def define (self, world):
		self.channel (world.marsOrbiter.phase, red, 0, 3, 50)
		self.channel (world.marsOrbiter.thrusterForce, lime, -1000, 1000, 50)
		self.channel (world.marsOrbiter.gravityForce, blue, 0, 10, 50)
		self.channel (world.marsOrbiter.velocity, yellow, 0, 20000, 50)
		self.channel (world.marsOrbiter.distance, white, 0, 1000000, 50)
		self.channel (world.marsOrbiter.run, maroon, 0, 1, 50)
		