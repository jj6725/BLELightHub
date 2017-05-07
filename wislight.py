##########################################################################################
# Wislight lightbulb commands
##########################################################################################
import pexpect
import time

class BulbWislight():
	DEVICE = "98:7B:F3:6C:0E:09"

	color = [0,0,0]
	brightness = 0

	def __init__(self):
		self.saveState()

	def sendCommand(self,cmd):
		cmd = list(cmd)
		package = ''.join('%02x'%x for x in cmd)
		command = "char-write-cmd 0x25 "+package
		print(command)
		child = pexpect.spawn("gatttool -I")
		child.sendline("connect {0}".format(self.DEVICE))
		child.expect("Connection successful", timeout=5)
		child.sendline(command)
		child.expect(pexpect.TIMEOUT, timeout=0.5)

	def saveState(self):
		command = "char-read-uuid 0xfff1"
		child = pexpect.spawn("gatttool -I")
		child.sendline("connect {0}".format(self.DEVICE))
		child.expect("Connection successful", timeout=5)
		child.sendline(command)
		child.expect("value:", timeout=5)
		child.expect("\r\n", timeout=5)
		state = child.before.split(' ')
		self.color[0] = int(state[2],16)
		self.color[1] = int(state[3],16)
		self.color[2] = int(state[4],16)
		self.brightness = int(state[5],16)
		return child.before

	def switchOn(self):
		if self.brightness == 0:
			self.brightness = 100
		self.sendCommand((0xa1, self.color[0], self.color[1], self.color[2], self.brightness))

	def switchOff(self):
		self.sendCommand((0xa1, self.color[0], self.color[1], self.color[2], 0x00))

	def setBrightness(self,value):
		self.sendCommand((0xa1, self.color[0], self.color[1], self.color[2], value))
		self.brightness = value
