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
import re
import subprocess
import time
import datetime

from AndroidAdapter.monkeydriver import *
from AndroidAdapter import screencapture

"""
ViewItem holds the information of single GUI component
"""
class ViewItem:

	def __init__(self, className, code, indent, properties, parent):
		self.__className = className
		self.__code = code
		self.__indent = indent
		self.__properties = properties
		self.__parent = parent
		self.__children = []
	
	def getClassName(self):
	
		return self.__className
	
	def getCode(self):
	
		return self.__code
	
	def getId(self):
	
		return self.getProperty("mID")
		
	def getText(self):
	
		return self.getProperty("mText")
	
	def getProperty(self, propertyName):
	
		if self.getProperties().has_key(propertyName):
			return self.getProperties()[propertyName]		
		return None
	
	def getIndent(self):
		return self.__indent
	
	def getProperties(self):
		return self.__properties
		
	def getParent(self):
		return self.__parent
		
	def addChild(self,child):
		self.__children.append(child)
	
	def getChildren(self):
		return self.__children
		

class GuiReaderError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


"""
GuiReader reads the contents of a GUI using the window service in the device.
"""
class GuiReader:

	PORT = 4939
	HOST = "localhost"
	DUMP_RETRIES = 5
	 
	def __init__(self, target, monkey, host = HOST, port = PORT):
		self.__host = host
		self.__port = port
		self.__root = None
		self.__items = []
		self.__target = target
		self.__monkey = monkey

	def readGUI(self):
	
		self.__items = []
		tried = 0
		while len(self.__items) == 0:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect( (self.__host, self.__port) )
			except socket.error,msg:
				print msg
				return False
			
			data = ''
			
			#DUMP -1 dumps the foreground window information
			try:
				sent = sock.send("DUMP -1\n")
				if sent == 0:
					sock.close()
					return False
				

				data = ""
				#Read whle the last line is "DONE"
				while True:
					
					try:
						newData = sock.recv(4096)
					except socket.timeout:
						continue

					data += newData
					if len(newData) < 4096 or newData.splitlines()[-1] == "DONE":
						break

				lines = data.splitlines()
				#If prosessing the screen dump fails, retry
				if not self.__processScreenDump__(lines):
										
					self.__items = []
					tried += 1
					time.sleep(0.2)
					if tried >= GuiReader.DUMP_RETRIES:
						sock.close()
						return False
					
				sock.close()
			except socket.error,msg:
				print msg
				return False
				
		return True

	
	#Processes the raw dump data and creates a tree of ViewItems
	def __processScreenDump__(self, dump):
		

		self.__items = []
		
		
		parent = None
		previousItem = None
		currentIndent = 0
		
		
		for line in dump:
			if (line == "DONE."):
				break
			
			#separate indent, class and properties for each GUI object
			matcher = re.compile("(?P<indent>\s*)(?P<class>[\w.$]+)@(?P<id>\w+) (?P<properties>.*)").match(line)	
			
			if not matcher:
				print "Invalid screen dump data while processing line: " + line
				return None
			
			#Indent specifies the hierarchy level of the object
			indent = len(matcher.group("indent")) 
			
			#If the indent is bigger that previous, this object is a child for the previous object
			if indent > currentIndent:
				parent = self.__items[-1]
				
			elif indent < currentIndent:
				for tmp in range(0,currentIndent - indent):
					parent = parent.getParent()
			
			currentIndent = indent
			
			propertiesData = matcher.group("properties")
			properties = {}
			index = 0
			
			#Process the properties of each GUI object
			while index < len(propertiesData):
				
				#separate name and value for each property
				propMatch = re.compile("(?P<prop>(?P<name>[^=]+)=(?P<len>\d+),)(?P<data>.*)").match(propertiesData[index:-1])
				
				if not propMatch or len(propMatch.group("data")) < int(propMatch.group("len")):
					print "Invalid screen dump data while processing line: " + line
					self.__items = None
					return None
				
				length = int(propMatch.group("len"))
					
				properties[propMatch.group("name")] = propMatch.group("data")[0:length]
				index += len(propMatch.group("prop")) + length + 1
				
			self.__items.append(ViewItem(matcher.group("class"),matcher.group("id"),indent,properties,parent))
			
			if parent:
				parent.addChild(self.__items[-1])
			
			if indent == 0:
				self.__root = self.__items[-1]
			
			
		return self.__items
	"""
	def printScreenDump(self):
		
		for i in self.__items:
			for tmp in range(0,i.getIndent()):
				print " ",

			print i.getClassName() + ":" + i.getId() + " id: "  + i.getProperties()["mID"],
			if i.getProperties().has_key("mText"):
				print " text: \"" + i.getProperties()["mText"] + "\"",
			print ""
			print i.getProperties()
	"""
	
	def printDump(self):

		self.__printChildren__(self.__root)
		
	
	#Takes a screenshot. TODO: EXPERIMENTAL! does not work well
	def takeScreenshot(self, out_path = None):
		
		if out_path == None:
		
			time = datetime.datetime.now()		
			month = "%.2d" % time.month
			day = "%.2d" % time.day
			hour = "%.2d" % time.hour
			min = "%.2d" % time.minute
			sec = "%.2d" % time.second
			
			out_path =  "screen_" + str(time.year) +  str(month) + str(day) + "-" + str(hour) + str(min) + str(sec) + ".png"

			
		screencapture.captureScreen(out_path, self.__target)
	
	
	#prints out the screen dump
	def __printChildren__(self, node):
		for tmp in range(0,node.getIndent()):
			print " ",
		print node.getClassName() + ":" + node.getId() + " id: "  + node.getProperties()["mID"],
		if node.getProperties().has_key("mText"):
			print " text: '" + node.getProperties()["mText"] + "'",
		print "coordinates:", node.getProperties()["mLeft"], node.getProperties()["mTop"], node.getProperties()["mRight"],node.getProperties()["mBottom"]
		for c in node.getChildren():
			self.__printChildren__(c)
	
	
	#Helper function for finding a listview from the GUI
	def getListView(self,rootItem = None):
		
		root = rootItem
		if not rootItem:
			root = self.__items[0]
			
		comp = lambda x: x.getClassName().find("ListView") != -1	
		
		return self.__findFirstItem__(root,comp)
		
	#searches a component that satisfies the given lamda comparator
	def findComponent(self, comparator, rootItem = None, searchAll = False):
	
		root = rootItem
		
		if self.__items == None or len(self.__items) == 0:
			return None
		
		if not rootItem:
			root = self.__items[0]

		if searchAll:
			return self.__findAllItems__(root, comparator)
		
		return self.__findFirstItem__(root, comparator)
	
	
	#Searches the GUI hiearhy for a object with a given text
	def findComponentWithText(self, text, roleName = "", rootItem = None, searchAll = False, partial = False):
		"""
		for i in self.__items:
			if i.getProperties().has_key("mText") and i.getProperties()["mText"].find(text) != -1:
				return i
				
		return None
		"""
		
		if roleName == None:
			roleName = ""
		if not partial:
			comp = lambda x: x.getClassName().find(roleName) != -1 and x.getProperties().has_key("mText") and x.getProperties()["mText"] == text	
		else:
			comp = lambda x: x.getClassName().find(roleName) != -1 and x.getProperties().has_key("mText") and x.getProperties()["mText"].find(text) != -1

		return self.findComponent(comp,rootItem,searchAll)
		
	#Searches the GUI hiearhy for a object with the given id
	def findComponentWithId(self, id, roleName = "", rootItem = None, searchAll = False):
	
		"""
		items = []
		for i in self.__items:
			if i.getProperties().has_key("mId") and i.getProperties()["mId"] == id:
			
				if searchAll:
					items.append(i)
				else:
					return i	
		
		if len(items) == 0:
			return None
			
		return items
		"""
		if roleName == None:
			roleName = ""
			
		#If id is empty, all components are accepted
		if id == "":
			comp = lambda x: x.getClassName().find(roleName) != -1 
		else:			
			comp = lambda x: x.getClassName().find(roleName) != -1 and x.getProperties().has_key("mID") and x.getProperties()["mID"] == id
	
		return self.findComponent(comp,rootItem,searchAll)

		
	#This method finds the coordinates of the foreground window.
	#TODO: Warning, very dependant on the dumsys command. If output is changed (likely between platform versions), the method will break!
	
	def __getForegroundWindowCoordinates__(self):
		
		retcode = subprocess.call("adb -s " + self.__target + " shell dumpsys window > windowinfo.txt",shell=True)
		
		if retcode != 0:
			print "Error when calling adb, make android sdk tools are in the path"
			exit()
		
		file = open("windowinfo.txt","r")
		windowInfo = file.read()
		
		focusId = "mCurrentFocus="
		focusIndex = windowInfo.find(focusId)
		
		if focusIndex != -1:
			currentWindowName = windowInfo[focusIndex + len(focusId) : windowInfo.find("\n",focusIndex)].strip()
			
			shownFrameText = "mShownFrame="
			windowListingIndex = windowInfo.find(currentWindowName)
			if windowListingIndex != -1:
				coordIndex = windowInfo.find(shownFrameText, windowListingIndex) + len(shownFrameText)
				try:
					return  eval(windowInfo[windowInfo.find("[",coordIndex) + 1 : windowInfo.find(",",coordIndex) ]) , eval(windowInfo[windowInfo.find(",",coordIndex) + 1 : windowInfo.find("]",coordIndex) ]) 
				except:
					errormessage = "error evaluating coordinates of focused window"
			
			else:
				errormessage = "'mShownFrame=' attribute not found"
			
		else:
			errormessage = "'mCurrentFocus=' attribute not found"
				
		print "Fatal error: reading foreground window coordinates failed!"	
		
		raise GuiReaderError("Error when reading 'shell dumpsys window' output: " + errormessage)
		

	
	def __findAllItems__(self,node, comparator):

		items = []
		if comparator(node) and node.getProperties()["getVisibility()"] == "VISIBLE":
			items.append(node)
		for c in node.getChildren():
			if c.getProperties().has_key("getVisibility()") and c.getProperties()["getVisibility()"] == "VISIBLE":
				items.extend(self.__findAllItems__(c,comparator))
		return items
	
	
	def __findFirstItem__(self,node,comparator):

		if comparator(node):
			return node
		for c in node.getChildren():
			if c.getProperties().has_key("getVisibility()") and c.getProperties()["getVisibility()"] == "VISIBLE":
				item = self.__findFirstItem__(c,comparator)
				if item: return item
			
		return None
	
	
	#Calculates absolute GUI object coordinates (middle) from parent and window coordinates
	def getViewCoordinates(self, view):

		left = int(view.getProperties()["mLeft"])
		top = int(view.getProperties()["mTop"])
		
		parent = view.getParent()
		while parent:

			left += int(parent.getProperties()["mLeft"]) - int(parent.getProperties()["mScrollX"])
			top += int(parent.getProperties()["mTop"]) - int(parent.getProperties()["mScrollY"])
			parent = parent.getParent()
		
		height = int(view.getProperties()["getHeight()"])
		width = int(view.getProperties()["getWidth()"])
		
		#Get absolute window coordinates. If the window is not full screen, they can be different that 0,0
		window_top_x, window_top_y = self.__getForegroundWindowCoordinates__()	
		
		windowheight = int(self.__items[0].getProperties()["getHeight()"])
		screenheight = int(self.__monkey.getScreenSize()[1])

		if window_top_y + top + height > windowheight:
			y = window_top_y + top + 1
			if y > screenheight:
				y = screenheight - 1

		elif top <= 0:
			y =  window_top_y + height - 1
		
		else: 
			y = window_top_y + top + (height) / 2
		
		x = window_top_x + left + (width) / 2
		
		print "Component found from coordinates: ",x,y
		return  x,y
		
	
	def getRoot(self):
		return self.__root
			
"""
if __name__ == "__main__":

	g = GuiReader()
	m = MonkeyDriver()
	m.connectMonkey()
	
	
	while True:
	
		kw = raw_input(">").strip()
		
		if (kw == "dump"):
			g.readGUI()
			g.printDump()
			continue

		name = kw.split(" ",1)[0]
		attr = kw.split(" ",1)[1]
		
		if name == "tap":
			g.readGUI()
			view = g.findComponentWithText(attr)
			if view:
				x , y = g.getViewCoordinates(view)
				print x , y
				m.sendTap(x,y)
			else:
				print "not found"
		if name == "press":
			m.sendPress(attr)
		
"""
