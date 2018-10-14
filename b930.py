##########################################################################################
# B930 lightbulb commands
##########################################################################################
import pexpect, random, time, argparse

class BulbB930():
	DEVICE = "F4:B8:5E:92:73:40"
	mode = ["Red","Green","Blue","Yellow","Pink","Light Blue","White RGB Mixer","RGB Mixer","Seven Color Mixer","RGB Gradual"]

	def sendCommand(self,cmd,rdcs = True):
		cmd = list(cmd)
		if rdcs:#random checksum
			cmd.append(random.randint(0,256))
			s = 28#checksum
			for i in cmd:
				s += i
				s = s&255
			cmd.append(s)
		
		cmd.append(0xd)
		package = ('aa0afc3a8601' + ''.join('%02x'%x for x in cmd))
		command = "char-write-cmd 0x21 "+package
		print(command)
		child = pexpect.spawn("gatttool -I")
		child.sendline("connect {0}".format(self.DEVICE))
		child.expect("Connection successful", timeout=5)
		child.sendline(command)
		child.expect(pexpect.TIMEOUT, timeout=0.5)

	def readState(self):
		command = "char-read-uuid 0xfff2"
		print(command)
		child = pexpect.spawn("gatttool -I")
		child.sendline("connect {0}".format(self.DEVICE))
		child.expect("Connection successful", timeout=5)
		child.sendline(command)
		child.expect("handle: 0x0024", timeout=5)
		child.expect("\r\n", timeout=5)
		print(child.before)
		return child.before

	def isNormalMode(self):
		hexVal = self.readState()
		hexVal = hexVal.replace(" ", "")
		if hexVal[11:17] == '808080' :
			return True
		else:
			return False

	def switchOn(self):
		self.sendCommand((0x0a, 0x01, 0x01, 0x00, 0x28), False)

	def switchOff(self):
		self.sendCommand((0x0a, 0x01, 0x00, 0x01, 0x28), False)

	def whiteReset(self):
		self.sendCommand((0x0d, 0x06, 0x02, 0x80, 0x80, 0x80, 0x80, 0x80))

	def setBrightness(self,value):
		self.sendCommand((0x0c, 0x01, value + 1))

	def setTemperature(self,value):
		self.sendCommand((0x0e, 0x01, (10-value) + 2))

	def setRGB(self, red, green, blue):
		self.sendCommand((0x0d, 0x06, 0x01, red&255, green&255,blue&255, 0x80, 0x80))

	def setPreset(self, value):
		self.sendCommand((0x0b, 0x01, value))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-r",type=int)
	parser.add_argument("-g",type=int)
	parser.add_argument("-b",type=int)
	parser.add_argument("-i",type=int)
	args = parser.parse_args()
	bulb = BulbB930
	# bulb().whiteReset()
	# bulb().setRGB(args.r,args.g,args.b)
	bulb().setBrightness(args.i)
	# bulb().switchOff()
	