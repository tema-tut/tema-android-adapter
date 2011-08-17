#!/usr/bin/env python
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


import sys
import os
sys.path.append(os.path.realpath(".."))

from AndroidAdapter import monkeydriver
import socket
from threading import Thread
import time
import unittest

# verdicts:

PASS,FAIL="PASS","FAIL"

        
class MockMonkey(Thread):

	def __init__(self):
		Thread.__init__(self)
	
	def close(self):
		self.run = False
		
		try:
			self.sock.close()
			self.conn.close()
		except:
			pass
	
	def run(self):
		self.run = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(("localhost", 4942))
		self.sock.settimeout(2)
		self.sock.listen(1)
		
		while self.run:
			try:
				self.conn, addr = self.sock.accept()

			except:
				continue
			
			connected = True
			while connected:
				try:
					data = self.conn.recv(2048).strip()
					print data
					if data == "getvar okvar":
						self.conn.sendall("OK:" + "hello")
					elif data == "getvar failvar":
						self.conn.sendall("ERR")
					
				except Exception,inst:
					connected = False
					self.conn.close()

				
		self.sock.close()
			

### UNIT TESTs for Monkeydriver

class TestMonkeyDriver(unittest.TestCase):

	
	def setUp(self):
		self.__monk = monkeydriver.MonkeyDriver(port = 4942)
		self.__monk.connectMonkey()
	
	def testMonkeyGetVariable(self):
		var = self.__monk.getVariable("okvar")
		self.assert_(var == "hello")
	
	def testMonkeyGetVariableFail(self):
		var = self.__monk.getVariable("failvar")
		self.assert_(var == None)
	
	
if __name__ == '__main__':
	
	mockm = MockMonkey()
	mockm.start()

	tests = unittest.TestLoader().loadTestsFromTestCase(TestMonkeyDriver)
	unittest.TextTestRunner(verbosity=2).run(tests)

	mockm.close()
