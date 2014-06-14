from SimPyLC import *

class WashingMachine (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		
		self.timer = Timer()
		self.door = Marker()
		self.lock = Marker()
		self.waterLevel = Register()
		self.waterInletStatus = Marker()
		self.drumRotationDirection = Marker()
		self.washingPowderInletStatus = Marker()
		self.drumSpeed = Register()
		self.waterDrainStatus = Marker()
		self.stage = Register()
		self.runner = Runner()
		
	def input (self, world):	
		pass
	
	def sweep (self):
		self.stage.set(0, self.stage == 0)
		self.timer.reset(not self.door)
		self.lock.mark(1, self.door and self.stage == 0)
		self.waterInletStatus.mark(1, self.lock and self.waterLevel < 200 and self.stage == 0, 0)
		self.washingPowderInletStatus.mark(1, self.lock and self.waterLevel < 200 and self.stage == 0, 0)
		self.waterLevel.set(self.waterLevel + 1, self.waterInletStatus)
		
		self.timer.reset(self.stage == 0 and self.waterLevel >= 200)
		self.stage.set(1, self.stage == 0 and self.waterLevel >= 200)	
		self.drumRotationDirection.mark(0, ((self.timer > 1 and self.timer < 2) or self.timer > 3) and self.stage == 1)
		self.drumRotationDirection.mark(1, (self.timer < 1 or (self.timer > 2 and self.timer < 3)) and self.stage == 1)
		self.drumSpeed.set(100, self.stage == 1)
				
		self.stage.set(2, self.stage == 1 and self.timer > 4)
		self.timer.reset(self.stage == 2 and self.timer > 4)
		self.waterDrainStatus.mark(1, self.stage == 2)
		self.waterLevel.set(self.waterLevel - 1, self.waterDrainStatus and self.stage == 2)
		
		self.timer.reset(self.stage == 2 and self.waterLevel <= 0)
		self.stage.set(3, self.stage == 2 and self.waterLevel <= 0)
		self.waterInletStatus.mark(1, self.lock and self.waterLevel < 200 and self.stage == 3, 0)
		self.waterLevel.set(self.waterLevel + 1, self.waterInletStatus)
		
		self.timer.reset(self.stage == 3 and self.waterLevel >= 200)
		self.stage.set(4, self.stage == 3 and self.waterLevel >= 200)	
		self.drumRotationDirection.mark(0, ((self.timer > 1 and self.timer < 2) or self.timer > 3) and self.stage == 4)
		self.drumRotationDirection.mark(1, (self.timer < 1 or (self.timer > 2 and self.timer < 3)) and self.stage == 4)
		self.drumSpeed.set(100, self.stage == 4)
		
		self.stage.set(5, self.stage == 4 and self.timer > 4)
		self.timer.reset(self.stage == 5 and self.timer > 4)
		self.waterDrainStatus.mark(1, self.stage == 5)
		self.waterLevel.set(self.waterLevel - 1, self.waterDrainStatus and self.stage == 5)
		self.waterLevel.set(self.waterLevel - 1, self.waterDrainStatus and self.stage == 5)
		
		self.timer.reset(self.stage == 5 and self.waterLevel <= 0)
		self.stage.set(6, self.stage == 5 and self.waterLevel <= 0)	
		self.waterDrainStatus.mark(1, self.stage == 6)
		self.drumRotationDirection.mark(0, ((self.timer > 1 and self.timer < 2) or self.timer > 3) and self.stage == 6)
		self.drumRotationDirection.mark(1, (self.timer < 1 or (self.timer > 2 and self.timer < 3)) and self.stage == 6)
		self.drumSpeed.set(300, self.stage == 6)	
		
		self.stage.set(7, self.stage == 6 and self.timer > 4)	
		self.timer.reset(self.stage == 7 and self.timer > 4 and self.drumSpeed == 300)
		self.waterDrainStatus.mark(1, self.stage == 7)
		self.drumRotationDirection.mark(0, ((self.timer > 1 and self.timer < 2) or self.timer > 3) and self.stage == 7)
		self.drumRotationDirection.mark(1, (self.timer < 1 or (self.timer > 2 and self.timer < 3)) and self.stage == 7)
		self.drumSpeed.set(500, self.stage == 7)
			
		self.stage.set(8, self.stage == 7 and self.timer > 4)
		self.timer.reset(self.stage == 8)
		self.lock.mark(0, self.stage == 8)			

		self.waterDrainStatus.mark(0, not (self.stage == 2 or self.stage == 5 or self.stage == 6 or self.stage == 7))
		self.drumSpeed.set(0, self.stage == 0 or self.stage == 2 or self.stage == 3 or self.stage == 5 or self.stage == 8)
	
	def output(self, world):
		pass
		