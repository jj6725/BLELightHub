from b930 import BulbB930
from wislight import BulbWislight
import time, argparse

class BulbManager():

	bulbA = BulbB930
	bulbB = BulbWislight

	def bulbsBrightness(self, value):
		self.bulbA().setBrightness(value)
		self.bulbB().setBrightness(int(value*255/10))

	def bulbsTemperature(self, value):
		self.bulbA().setTemperature(value)

	def bulbsOn(self):
		self.bulbA().switchOn()
		self.bulbB().switchOn()

	def bulbsOff(self):
		self.bulbA().switchOff()
		self.bulbB().switchOff()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i",type=int)
	args = parser.parse_args()
	bulbs = BulbManager
	if(args.i == 0):
		bulbs().bulbsOff()
	else:
		bulbs().bulbsOn()
		bulbs().bulbsBrightness(args.i)
