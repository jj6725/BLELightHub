from b930 import BulbB930
from wislight import BulbWislight
import time

class BulbManager():

	bulbA = BulbB930
	bulbB = BulbWislight

	def bulbsBrightness(self, value):
		self.bulbA().setBrightness(value)
		self.bulbB().setBrightness(value*25)

	def bulbsTemperature(self, value):
		self.bulbA().setTemperature(value)
		
	def bulbsOn(self):
		self.bulbA().switchOn()
		self.bulbB().switchOn()

	def bulbsOff(self):
		self.bulbA().switchOff()
		self.bulbB().switchOff()