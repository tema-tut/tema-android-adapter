# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010 Tampere University of Technology
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import socket

"""
MonkeyDriver communicates with the Monkey tool network interface. Requires 
platfrom version 1.6 or later
"""
class MonkeyDriver:

	PORT = 1080
	HOST = "localhost"
	
	def __init__(self, port = PORT, host = HOST):
		self.host = host
		self.port = port
		self.__isConnected = False

	def connectMonkey(self):
	
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect( (self.host, self.port) )
			self.__isConnected = True
			return True
		except socket.error,msg:
			print msg
			return False
	
	
	#Gets a system variable.
	#If variable_name is not defined, returns None
	def getVariable(self, variable_name):
		if not self.__isConnected:
			return None
	
		try:
			self.sock.send("getvar " + variable_name + "\n")	
			data = self.sock.recv(4096).strip()
			if not data.startswith("OK:"):
				return None
			return data.split("OK:")[1]
			
		except socket.error:
			self.sock.close()
			self.__isConnected = False
			return None
		
	
	def getScreenSize(self):
		try:
			height = int(self.getVariable("display.height"))
			width = int(self.getVariable("display.width"))
		
		except TypeError:
			return None,None
			
		return width,height
	
	def getPlatformVersion(self):
	
		return self.getVariable("build.version.release")
	
	def __sendCommand__(self,command):
		if not self.__isConnected:
			return False
		try:
			self.sock.send(command + "\n")	
			data = self.sock.recv(4096).strip()
			if data == "OK":
				return True
			return False
		except socket.error:
			self.sock.close()
			self.__isConnected = False
			return False
		

	def sendTap(self,xCoord,yCoord):
		return self.__sendCommand__("tap " + str(xCoord) + " " + str(yCoord))	
		
	def sendKeyUp(self,key):
		return self.__sendCommand__("key up " + key)
		
	def sendKeyDown(self,key):
		return self.__sendCommand__("key down " + key)
	
	def sendTouchUp(self,xCoord,yCoord):
		return self.__sendCommand__("touch up " + str(xCoord) + " " + str(yCoord))
	
	def sendTouchDown(self,xCoord,yCoord,):
		return self.__sendCommand__("touch down " + str(xCoord) + " " + str(yCoord))
	
	def sendTouchMove(self,xCoord,yCoord,):
		return self.__sendCommand__("touch move " + str(xCoord) + " " + str(yCoord))
	
	def sendTrackBallMove(self,dx,dy):
		return self.__sendCommand__("trackball " + str(dx) + " " + str(dy))
	
	def sendPress(self, key):
		return self.__sendCommand__("press " + key)
	
	def sendType(self, text):
		return self.__sendCommand__("type " + text)
	
	def closeMonkey(self):
		pass
		

