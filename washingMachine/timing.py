from SimPyLC import *

class Timing (Chart):
	def __init__ (self, name):
		Chart.__init__ (self, name)
		
	def define (self, world):
		self.channel (world.washingMachine.timer, red, 0, 20, 50)
		self.channel (world.washingMachine.door, lime, 0, 1, 50)
		self.channel (world.washingMachine.lock, blue, 0, 1, 50)
		self.channel (world.washingMachine.waterLevel, yellow, 0, 250, 50)
		self.channel (world.washingMachine.waterInletStatus, white, 0, 1, 50)
		self.channel (world.washingMachine.drumRotationDirection, maroon, 0, 1, 50)
		self.channel (world.washingMachine.washingPowderInletStatus, green, 0, 1, 50)
		self.channel (world.washingMachine.drumSpeed, navy, 0, 500, 50)
		self.channel (world.washingMachine.waterDrainStatus, fuchsia, 0, 1, 50)
		self.channel (world.washingMachine.stage, purple, 0, 7, 50)
		