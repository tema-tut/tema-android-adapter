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

import re
import time
import subprocess
import socket
import ConfigParser

from adapterlib.keyword import Keyword

import AndroidAdapter.guireader as guireader
from AndroidAdapter.object_keyword import ObjectKeyword

TAP_INTERVAL = 0.2 #s
NAV_DELAY = 0.5 #s


#-----------------------------------------------------------------------------#

class VerifyText(ObjectKeyword):

	"""
	Verifies if the given text is found from the screen from some GUI object.

    If <NoUpdate> -parameter is given, the keyword will not update the GUI
    hierarchy, but uses the previous update. This can be used to make execution
    faster
	
	If "partial:" parameter is given, the search accepts components where the 
    text is found somewhere inside its text content.
	
	Usage::

		VerifyText [<NoUpdate>][partial:]'text',[object]
	"""
	
	def __init__(self):
		super(VerifyText,self).__init__()
		#TODO: Not completed pattern!
		pattern = re.compile("(<(?P<style>[^>]+)>\s+)?(?P<partial>partial:)?\'(?P<text>.*)\'(\s*,\s*(?P<component>" + self.componentPattern + "))?")
		self.attributePattern = pattern
		self.delay = -1	  
				  
	def execute(self):
		matcher = self.attributePattern.match(self.attributes)
		self.log('text: ' + matcher.group("text"))
		
		#No component specified
		if(matcher.group("component") == None):
			self.log("Searching from first component showing")
			return self.verifyText(matcher.group("text"),partial = (matcher.group("partial") != None), style = matcher.group("style"))
		#Component and rolename specified       
		componentName, rolename = self.matchComponent(matcher.group("component"))
		if(componentName == None):
			return False
		
		self.log("component: " + componentName)
		if(rolename != None):
			self.log("rolename: " + rolename)
		
		
		
		result = self.verifyText(matcher.group("text"), componentName, rolename, partial = (matcher.group("partial") != None),style = matcher.group("style") )    
		return result
			  
			  
	def verifyText(self, text, rootName="", rolename="", searchNodes = None, partial = False, style = None):
		"""
		Searches the given string under the given node(s).
		
		@type text: string
		@param text: Text that is searched.
		
		@type rootName: string
		@param rootName: Reference to the component that is used as a root for the search
		
		@type rolename: string
		@param rolename: rolename of the search root component (to identify better)
		
		@type searchNodes: list
		@param searchNodes: List of ViewItems. If given, this list is used as search roots for
		the search, and the rootName and rolename parameters are omitted. Giving the nodes
		this way enhanches the performance greatly if multiple verifys are done in a row.
		(i.e. waitText)
		
		@rtype: boolean or "ERROR"
		@return: True if text was found, false if text was not found and "ERROR" if fatal
		errors occured in the search.
		
		"""
		
		if style != "NoUpdate":	
				self._target.getGUIReader().readGUI()
		
		rootNodes = searchNodes
		if searchNodes == None:
			rootNodes = []
			if rootName == 'root' or rootName == '':
				rootNodes.append(self.searchroot)
			else:
				rootNodes = self.findComponent(rootName, rolename, True)   
		if(rootNodes == None or len(rootNodes) == 0):
			self.log("Root node for verification not found")
			return False

		else:  
				
			for node in rootNodes:
				#self.log("Searching text: \"" + text + "\" below the node: " + node.name)     
				#Check children
				#if self.findText(text, node,regex):
				#	return True
				if self._target.getGUIReader().findComponentWithText(text, rolename, node, partial = partial) != None:
					return True
				
			return False

#-----------------------------------------------------------------------------# 

class WaitText(VerifyText):
	
	"""
	WaitText waits that a desired text appears on screen. Uses Verify text 
    methods to find the text.
	
	If "regex:" parameter is given, the text parameter is treated as a regular
    expression.	If any text found mathes with the expression, the keyword 
    returns true 
	
	Usage:
		kw_WaitText [regex:]'text',[timeout],[componentReference]
	
	"""
	
	def __init__(self):
		super(WaitText,self).__init__()
		#TODO: Not completed pattern!
		#kw_WaitText 'text',[waittime],component[;rolename]
		pattern = re.compile('(?P<partial>partial:)?\'(?P<text>.+)\'(\s*,\s*(?P<time>\d+))?(\s*,\s*(?P<component>' + self.componentPattern + '))?')
		self.attributePattern = pattern
		self.__time = 10 #Default time

	def execute(self):

		matcher = self.attributePattern.match(self.attributes)
		self.log('text: ' + matcher.group("text"))
		
		if matcher.group("component"):
			componentName, rolename = self.matchComponent(matcher.group("component"))
			if(componentName == None):
				return False
		else:
			componentName = "root"
			rolename = ""
		
		self.log("component: " + componentName)
		if(rolename != None):
			self.log("rolename: " + rolename)       
		
		self.__time = matcher.group("time")
		if(self.__time == None):
			self.__time = 10
		else:
			self.__time = int(self.__time)    
		self.log("wait-time: " + str(self.__time))        
	

		#Search node is searched here to optimate the verification
		#TODO: Create a function for this in Keyword-class
		"""
		searchNodes = []
		if componentName == 'root':
			searchNodes.append(self.searchroot)
		elif componentName.strip() == "":
			searchNodes.append(self.findFirstNodeShowing());  
		else:
			searchNodes = self.findComponent(componentName, rolename, True)      
		if searchNodes == None:
		   self.log("Root node for verification not found") 
		   return False
		"""

		counter = 1
		result = False
		searchTime = int(time.time()) + self.__time
		while int(time.time()) <= searchTime:
			try:
				result = self.verifyText(matcher.group("text"), componentName, rolename, searchNodes = None, partial  = matcher.group("partial") != None )
				#result = self.verifyText(matcher.group(1), searchNodes = searchNodes)
				
				print "search nro:" + str(counter)
				counter = counter + 1
			except Exception: 
				pass    
			if result:
				break 
			time.sleep(0.2)    
		return result
		   
#-----------------------------------------------------------------------------#

class WaitObject(VerifyText):
	
	"""
	Kw_WaitText waits that a desired object appears on screen.
	

	
	Usage:
		kw_WaitObject [timeout,]componentReference
	
	"""
	
	def __init__(self):
		super(WaitObject,self).__init__()		
		#TODO: Not completed pattern!
		#kw_WaitText 'text',[waittime],component[;rolename]
		pattern = re.compile('((?P<time>\d+)\s*,\s*)?(?P<component>' + self.componentPattern + ')')
		self.attributePattern = pattern
		self.__time = 10 #Default time

	def execute(self):

		matcher = self.attributePattern.match(self.attributes)
		
		self.__time = matcher.group("time")
		if(self.__time == None):
			self.__time = 10
		else:
			self.__time = int(self.__time)    
		self.log("wait-time: " + str(self.__time))        
	

		counter = 1
		result = False
		searchTime = int(time.time()) + self.__time
		while int(time.time()) <= searchTime:
			try:
				result = self.findComponentReference(matcher.group("component")) != None
				print "search nro:" + str(counter)
				counter = counter + 1
			except Exception: 
				pass    
			if result:
				break 
			time.sleep(0.2)    
		return result
		   
#-----------------------------------------------------------------------------#


class SelectFromList(ObjectKeyword):
	
	"""
	Selects an item from a vertical list of items.
	
	Usage:
		
		kw_SelectFromList 'list_item'
	
	"""
	
	def __init__(self):
		super(SelectFromList,self).__init__()
		pattern = re.compile('\'(?P<item>.*)\'(\s*,\s*(?P<execute>(true|false)))?')
		self.attributePattern = pattern

	def __getSelectedIndex__(self):
	
		list = None
		selectedIndex = None
		try:
			self._target.getGUIReader().readGUI()
			list = self._target.getGUIReader().getListView()
			if not list:
				print "No ListView found from the screen"
				return None, None
			
			selectedIndex = int(list.getProperties()["mSelectedPosition"])
		except ValueError:
			return None, None
		return list, selectedIndex

	def execute(self):
		
		
		matcher = self.attributePattern.match(self.attributes)
		self.log('item: ' + matcher.group("item"))
		executeItem = matcher.group("execute") == None or matcher.group("execute") == "true"
		
		list, selectedIndex = self.__getSelectedIndex__()
		if list == None:
			return False
		#gui not found
		
		#Give focus to an item in the list
		while selectedIndex == -1:
			if not self._target.getMonkeyDriver().sendPress("DPAD_DOWN"):
				return False
				
			list, selectedIndex = self.__getSelectedIndex__()
			if list == None:
				return False
		
		item = self._target.getGUIReader().findComponentWithText(matcher.group("item"), rootItem = list, searchAll = False)
		
		#Selected item's index relative to currently shown list part
		RelIndex = 0
		for c in list.getChildren():
			if self._target.getGUIReader().findComponent(lambda x: x.getProperties().has_key("isSelected()") and x.getProperties()["isSelected()"].lower() == "true", c, False):
				break
			RelIndex +=1
		
		
		#Scroll list to the top if not already and if the item was not found from the current list part
		if selectedIndex > 0 and item == None and RelIndex != selectedIndex:
			for i in range(0,selectedIndex):
				if not self._target.getMonkeyDriver().sendPress("DPAD_UP"):
					return False
			time.sleep(NAV_DELAY)
			self._target.getGUIReader().readGUI()
		

		#Scroll the list down until the item is seen, or the bottom of the list is reached
		while item == None:	
					
			list = self._target.getGUIReader().getListView()
			item = self._target.getGUIReader().findComponentWithText(matcher.group("item"), rootItem = list, searchAll = False)
			selectedIndex = int(list.getProperties()["mSelectedPosition"])
			
			if item:
				break

			RelCurrentIndex = 0
			for c in list.getChildren():
				if self._target.getGUIReader().findComponent(lambda x: x.getProperties().has_key("isSelected()") and x.getProperties()["isSelected()"].lower() == "true", c, False):
					break
				RelCurrentIndex += 1

			
			#If last item of the list is listed, item can't be found
			if selectedIndex + (len(list.getChildren()) - RelCurrentIndex) >= int(list.getProperties()["mItemCount"]):
				return False
			
	
			#TODO: Too much scrolling in some situations.
			for i in range(0,len(list.getChildren())):
				if not self._target.getMonkeyDriver().sendPress("DPAD_DOWN"):
					return False
					
			time.sleep(NAV_DELAY)
			self._target.getGUIReader().readGUI()

		#If item was found, tap it...
		if item:
		
			#...only if execute parameter allows
			if executeItem:
			
				try:
					x,y = self._target.getGUIReader().getViewCoordinates(item)
				except guireader.GuiReaderError,e:
					print e
					return False
				
				return self._target.getMonkeyDriver().sendTap(x,y)
			
			#else make sure the item is in the selected state
			else:
			
				currentRelIndex = 0
				currentFound = False
				itemRelIndex = 0
				itemFound = False
				
				for c in list.getChildren():
				
					if self._target.getGUIReader().findComponentWithText(matcher.group("item"), rootItem = c) != None:
						itemFound = True 
					elif not itemFound:
						itemRelIndex += 1
						
					if c.getProperties()["isSelected()"] == "true":
						currentFound = True 
					elif not currentFound:
						currentRelIndex += 1

				press = "DPAD_DOWN"
				if itemRelIndex < currentRelIndex:
					press = "DPAD_UP"
					
				while item.getProperties()["isSelected()"] == "false":
					if not self._target.getMonkeyDriver().sendPress(press):
						return False
					time.sleep(NAV_DELAY)	
					self._target.getGUIReader().readGUI()	
					list = self._target.getGUIReader().getListView()
					item = self._target.getGUIReader().findComponentWithText(matcher.group("item"), rootItem = list, searchAll = False)
					if not item:
						return False
						
	
			return True	
		
			"""
			#This implementation navigates to the desired item with dpad. It does not work if the list contains items that are not focusable.
			
			RelItemIndex = 0 
			for c in list.getChildren():
				if self._target.getGUIReader().findComponentWithText(matcher.group("item"), rootItem = c, searchAll = False):
					break
				RelItemIndex +=1
			
			RelCurrentIndex = 0
			for c in list.getChildren():
				if self._target.getGUIReader().findComponent(lambda x: x.getProperties().has_key("isSelected()") and x.getProperties()["isSelected()"].lower() == "true", c, False):
					break
				RelCurrentIndex +=1
			
			steps = RelItemIndex - RelCurrentIndex
			
			if steps > 0:
				key = "DPAD_DOWN"
			else:
				key = "DPAD_UP"
			
			for i in range(0,abs(steps)):
				if not self._target.getMonkeyDriver().sendPress(key):
					return False	
					
			if not self._target.getMonkeyDriver().sendPress("DPAD_CENTER"):
				return False	
				
			return True   
			"""
			
		return False
				
	
#-----------------------------------------------------------------------------#  

class TapCoordinate(Keyword):
	
	def __init__(self):
		super(TapCoordinate,self).__init__()
		pattern = re.compile("(?P<x>\d+)\s*,\s*(?P<y>\d+)(\s*,\s*(?P<times>\d+))?")       
		self.attributePattern = pattern   
				  
	def doTap(self,x,y):
		
		w, h = self._target.getMonkeyDriver().getScreenSize()
		if (int(x) > w or int(y) > h):
			print "Invalid coordinates"
			return False
		
		return self._target.getMonkeyDriver().sendTap(x,y)	
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		times = 1
		
		if matcher.group("times"):
			times = int(matcher.group("times"))
			
		for i in range(0,times):
			if not self.doTap(matcher.group(1),matcher.group(2)):
				return False
		
		return True
#-----------------------------------------------------------------------------# 

class TapDownCoordinate(TapCoordinate):
	
	def doTap(self,x,y):
		return self._target.getMonkeyDriver().sendTouchDown(x,y)	
	

#-----------------------------------------------------------------------------# 

class TapUpCoordinate(TapCoordinate):
	
	def doTap(self,x,y):
		return self._target.getMonkeyDriver().sendTouchUp(x,y)	

#-----------------------------------------------------------------------------# 

class LongTapCoordinate(TapCoordinate):
	
	def doTap(self,x,y):
	
		if self._target.getMonkeyDriver().sendTouchDown(x,y):
			time.sleep(self.__hold_time)
			return self._target.getMonkeyDriver().sendTouchUp(x,y)
		return False
		
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		self.__hold_time = 2
		
		if matcher.group("times"):
			self.__hold_time = int(matcher.group("times"))

		if not self.doTap(matcher.group(1),matcher.group(2)):
			return False
		
		return True

#-----------------------------------------------------------------------------#

class MoveToCoordinate(TapCoordinate):
	
	def doTap(self,x,y):
		return self._target.getMonkeyDriver().sendTouchMove(x,y)	

	
#-----------------------------------------------------------------------------#  

class TapObject(ObjectKeyword):
	
	"""
	Taps the given component.
	
	Usage:
		kw_TapObject componentReferece
	"""
	
	def __init__(self):
		super(TapObject,self).__init__()
		pattern = re.compile("((?P<times>\d+)\s*,\s*)?(?P<component>" + self.componentPattern + ")")
		self.attributePattern = pattern  
	
	def doTapAction(self,x,y):
		return self._target.getMonkeyDriver().sendTap(x,y)	
	
	def doTap(self,reference, times = 1):	
	
		item = self.findComponentReference(reference)
		
		if not item:
			return False	
		
		try:
				
			x,y = self._target.getGUIReader().getViewCoordinates(item)
		except guireader.GuiReaderError,e:
			print e
			return False
		
		for i in range(0,times):
			if not self.doTapAction(x,y):
				return False
			if times > 1:
				time.sleep(TAP_INTERVAL)
		return True
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes)
		
		times = 1
		if matcher.group("times"):
			times = int(matcher.group("times"))
		
		return self.doTap(matcher.group("component"),times)	 
		
		

#-----------------------------------------------------------------------------# 

class TapDownObject(TapObject):
	
	def doTapAction(self,x,y):
		return self._target.getMonkeyDriver().sendTouchDown(x,y)	
	

#-----------------------------------------------------------------------------# 

class TapUpObject(TapObject):
	
	def doTapAction(self,x,y):
		return self._target.getMonkeyDriver().sendTouchUp(x,y)	

#-----------------------------------------------------------------------------# 

class LongTapObject(TapObject):
	
	def doTapAction(self,x,y):
	
		if self._target.getMonkeyDriver().sendTouchDown(x,y):
			time.sleep(self.__hold_time)
			return self._target.getMonkeyDriver().sendTouchUp(x,y)
		return False
	
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes)
		
		times = 1
		self.__hold_time = 2
		if matcher.group("times"):
			self.__hold_time = int(matcher.group("times"))
		
		return self.doTap(matcher.group("component"),times)	
	
#-----------------------------------------------------------------------------# 

class MoveToObject(TapObject):
	
	def doTapAction(self,x,y):
		return self._target.getMonkeyDriver().sendTouchMove(x,y)	


#-----------------------------------------------------------------------------#     

class Drag(ObjectKeyword):
	
	def __init__(self):
		super(Drag,self).__init__()
		pattern = re.compile("((?P<coord1>(?P<x1>\d+)\s*,\s*(?P<y1>\d+))|(?P<component1>.+))\s*-->\s*((?P<coord2>(?P<x2>\d+)\s*,\s*(?P<y2>\d+))|(?P<component2>.*))")       
		self.attributePattern = pattern   
		self._holdtime = 2
		self._dragtime = 0.001
		self._movepoints = 20
				  
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		
		if matcher.group("coord1"):
			x1 = int(matcher.group("x1"))
			y1 = int(matcher.group("y1"))
		else:
		
			item = self.findComponentReference(matcher.group("component1").strip())
			if not item:
				return False
	
			try:	
				x1,y1 = self._target.getGUIReader().getViewCoordinates(item)
			except guireader.GuiReaderError,e:
			
				print e
				return False
		
		#Tap down the first coordinate
		if not self._target.getMonkeyDriver().sendTouchDown(x1,y1):
			return False
		
		
		if matcher.group("coord2"):
			x2 = int(matcher.group("x2"))
			y2 = int(matcher.group("y2"))
			time.sleep(self._holdtime)
		else:
					
			item = self.findComponentReference(matcher.group("component2").strip())
			if not item:
				return False
			try:
				
				x2,y2 = self._target.getGUIReader().getViewCoordinates(item)			
			except guireader.GuiReaderError,e:
				print e
				return False
		
		#Move to the second coordinate and tap up
		for i in range(0,self._movepoints):

			if x2 > x1:
				nx = x1 + ((x2-x1)/self._movepoints)*i
			else:
				nx = x1 - ((x1 -x2)/self._movepoints)*i
				
			if x2 > x1:
				ny = y1 + ((y2-y1)/self._movepoints)*i
			else:
				ny = y1 - ((y1 -y2)/self._movepoints)*i

			#print nx,ny
			if not self._target.getMonkeyDriver().sendTouchMove(nx,ny):
				return False
				
			#time.sleep(self._dragtime)
			
		if self._target.getMonkeyDriver().sendTouchUp(x2,y2):
			return True
		
		return False
		
#-----------------------------------------------------------------------------# 

class TouchScroll(Drag):
	
	def __init__(self):
		super(TouchScroll,self).__init__()
		self._holdtime = 0
				  
				  
		
#-----------------------------------------------------------------------------# 


class MoveTrackBall(Keyword):
	
	
	"""
	Taps the given component.
	
	Usage:
		kw_TapObject componentReferece
	"""
	
	def __init__(self):
		super(MoveTrackBall,self).__init__()
		pattern = re.compile("(?P<dx>(-)?\d+)\s*,\s*(?P<dy>(-)?\d+)")
		self.attributePattern = pattern  
	
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes)
		
		return self._target.getMonkeyDriver().sendTrackBallMove(matcher.group("dx"),matcher.group("dy"))


#-----------------------------------------------------------------------------#     

class SelectFromMenu(TapObject):
	
	"""
	Selects an item from the menu. 
	
	Presses the menu button, and finds the desired item. If the menu does not fit entirely to the screen and contains a "more" option, the item is searched under that menu. If the item is not found, menu will be closed in the end.
		
	Usage:

	"""
	
	def __init__(self):
		super(SelectFromMenu,self).__init__()
		pattern = re.compile("(?P<menu>'.*')")
		self.attributePattern = pattern  
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes)
		
		item = matcher.group("menu")
		
		if not self._target.getMonkeyDriver().sendPress("menu"):
			return False
			
		time.sleep(2)
		
		self._target.getGUIReader().readGUI()
		
		if self.doTap(item):
			result = True
		
		elif self.doTap("'More'"):
			self._target.getGUIReader().readGUI()
			result = self.doTap(item)
		
		else:
			result = False
		
		if not result:
			self._target.getMonkeyDriver().sendPress("menu")
			
		return result     
		
		
#-----------------------------------------------------------------------------# 

class IsTrue(Keyword):
    """
    Kw_IsTrue returns True or False depending on the parameter
    
    Usage::

        kw_IsTrue True
        kw_IsTrue False
    """
    def __init__(self):
        super(IsTrue,self).__init__()
        pattern = re.compile("((True)|(False))?")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False
        
    def execute(self):

        matcher = self.attributePattern.match(self.attributes)
        if(matcher.group(2) != None):
            return True
        return False   

#-----------------------------------------------------------------------------#

class SetTarget(Keyword):

    def __init__(self):
        super(SetTarget,self).__init__()
        pattern = re.compile(".*")
        self.attributePattern = pattern
        self.delay = -1
        
    def execute(self):
        return True  

#-----------------------------------------------------------------------------#          


class UpdateScreen(Keyword):

    def __init__(self):
        super(UpdateScreen,self).__init__()
        pattern = re.compile("\s*")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False
        
    def execute(self):
        self._target.getGUIReader().readGUI()
        return True  

#-----------------------------------------------------------------------------# 


class Delay(Keyword):

    def __init__(self):
        super(Delay,self).__init__()
        pattern = re.compile("(\\d.)?\\d+")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False
        
    def execute(self):

        matcher = self.attributePattern.match(self.attributes)
        if(matcher.group(0) != None):
            time.sleep(eval(matcher.group(0)))
            return True
        return False  

#-----------------------------------------------------------------------------#

class Type(Keyword):
	"""
	Inserts text into a component. 
	Returns false if the component does not support text editation.
	
	Usage:
		kw_Type 'text', componentReference
	"""
	def __init__(self):
		super(Type,self).__init__()		
		pattern = re.compile("'(.*)\'")#(\s*,\s*(" + self.componentPattern + "))")
		self.attributePattern = pattern   
				  
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		text = matcher.group(1)
		words = text.split(' ')
		
		first = True
		
		for word in words:
			
			if not first:
			
				if not self._target.getMonkeyDriver().sendPress("space"):
					return False
		
			if word != '':
				if not self._target.getMonkeyDriver().sendType(word): 
					return False
			
			first = False
			
		return True
		
#-----------------------------------------------------------------------------# 

class PressKey(Keyword):

	"""
	Presses and releases a key
	
	Usage:
		 Kw_PressKey keyname      
	"""
	
	def __init__(self):
		super(PressKey,self).__init__()
		pattern = re.compile("(?P<button>\w+)(\s*,\s*(?P<times>\d+))?")      
		self.attributePattern = pattern
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes) 
		times = 1
		
		if matcher.group("times"):
			times = int(matcher.group("times"))

		for i in range(0,times):
			if not self._target.getMonkeyDriver().sendPress(matcher.group(1)):
				return False
		
		return True

#-----------------------------------------------------------------------------# 
#Alias
class PressHardKey(PressKey):
	pass

#-----------------------------------------------------------------------------# 

class PressKeyUp(PressKey):
	"""
	releases a key
	
	Usage:
		 Kw_PressKeyUp keyname      
	"""
	
	def __init__(self):
		super(PressKeyUp,self).__init__()
		pattern = re.compile("(?P<button>\w+)")      
		self.attributePattern = pattern
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes) 

		return self._target.getMonkeyDriver().sendKeyUp(matcher.group(1))

		

#-----------------------------------------------------------------------------# 

class PressKeyDown(PressKey):

	"""
	presses and holds a key
	
	Usage:
		 Kw_PressKeyDown keyname      
	"""
	
	def __init__(self):
		super(PressKeyDown,self).__init__()
		pattern = re.compile("(?P<button>\w+)")      
		self.attributePattern = pattern
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes) 

		return self._target.getMonkeyDriver().sendKeyDown(matcher.group(1))

#-----------------------------------------------------------------------------# 


class LongPressKey(PressKey):
	"""
	    
	"""
	
	def __init__(self):
		super(LongPressKey,self).__init__()
		pattern = re.compile("(?P<button>\w+)(\s*,\s*(?P<time>\d+))?")      
		self.attributePattern = pattern
				  
	def execute(self):

		matcher = self.attributePattern.match(self.attributes) 
		hold_time = 2
		
		if matcher.group("time"):
			hold_time = int(matcher.group("time"))


		if not self._target.getMonkeyDriver().sendKeyDown(matcher.group(1)):
			return False
			
		time.sleep(hold_time)
		
		return self._target.getMonkeyDriver().sendKeyUp(matcher.group(1))
		
#-----------------------------------------------------------------------------# 

class CheckProperty(ObjectKeyword):
	
	"""

	
	"""
	
	def __init__(self):
		super(CheckProperty,self).__init__()
		pattern = re.compile('(?P<property>[^,]*)\s*,\s*\'(?P<value>.*)\'\s*,\s*(?P<component>' + self.componentPattern+ ')')
		self.attributePattern = pattern
				  
	def execute(self):
		
		matcher = self.attributePattern.match(self.attributes)
		property = matcher.group("property")
		value = matcher.group("value")	
		component = self.findComponentReference(matcher.group("component"))
		if component == None:
			return False
				
		if component.getProperties().has_key(property) and component.getProperties()[property] == value:
			return True
		
		return False       
		   
#-----------------------------------------------------------------------------# 


class LaunchApp(ObjectKeyword):
	
	"""
	LaunchApp 'package.Activity'
	
	"""
	
	def __init__(self):
		super(LaunchApp,self).__init__()	
		pattern = re.compile('\'((?P<class>(?P<package>[^:]*)(::(?P<activityOtherPackage>.+)|(?P<activitySamePackage>\.[^.]+)))|(?P<launchplace>(recent|appmenu):)?(?P<appname>[^\.]*))\'')
		#pattern = re.compile("'(?P<name>.*)'")
		self.attributePattern = pattern
		self.delay = 5
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
	
		config = ConfigParser.ConfigParser()
		
		#If the application has a specified launchup name, use that instead. 
		try:
			config.read("appconfig.ini")			
			launchname = config.get("Applications", matcher.group(1))

			if launchname:
				self.attributes = "'" + launchname + "'"
			
		except ConfigParser.Error:
			self.log("Application name not found from config, using the name directly")
		
	
		matcher = self.attributePattern.match(self.attributes)
		self.log('Launching activity: ' + matcher.group(0))
				
		
		#Launching application process directly
		if matcher.group("class"):
			try:
				#activity in the same package with the process
				activity = matcher.group('activitySamePackage')
				
				#Activity in a other package than the process
				if not activity:
					activity = matcher.group('activityOtherPackage')
			
				retcode = subprocess.call("adb -s " + self._target.name + " shell am start -n " + matcher.group('package') + "/" + activity, shell=True)
			except (OSError, ValueError):
				return False
			
			if retcode != 0:
				self.log("Launching application failed, check that android sdk tools are in the path variable")
				return False
			
			return True
		
		#Launching application through the GUI
		else:
		
			appname = matcher.group("appname")
			
			#Try launching from recent applications window
			if not matcher.group("launchplace") == "appmenu:":

				kw = LongPressKey()
				kw.initialize('home', self._target)
				if not kw.execute():
					return False
				time.sleep(1)
				kw = TapObject()
				kw.initialize("'" + appname +"'", self._target)
				if kw.execute():
					return True
				else:
					self._target.getMonkeyDriver().sendPress('back')
			
			#Try launching from the application menu
			if not matcher.group("launchplace") == "recent:":
	
				if not self._target.getMonkeyDriver().sendPress('home'):
					return False
				#TODO: Better solution?
				time.sleep(1)

				#TODO: Platform version dependant, Yuck!
				appsButton = 'id/all_apps'
				appsGrid = 'id/content'
					
					
				if self._target.getMonkeyDriver().getPlatformVersion() == "2.2":
				
					appsButton = 'id/all_apps_button'
					appsGrid = 'id/all_apps_2d_grid'
				
				
				kw = TapObject()
				kw.initialize(appsButton,self._target)
				if not kw.execute():
					return False
				
				kw = TapObject()
				kw.initialize(appsGrid + '::\'' + appname + '\'',self._target)
				if not kw.execute():
					return False
	
				return True
				
			return False

   
#-----------------------------------------------------------------------------# 

class ObjectVisible(ObjectKeyword):

	def __init__(self):
		super(ObjectVisible,self).__init__()
		pattern = re.compile('(?P<component>' + self.componentPattern+ ')')
		self.attributePattern = pattern
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		
		component = self.findComponentReference(matcher.group("component"))
		if component == None:
			return False
				
		if component.getProperties().has_key('getVisibility()') and component.getProperties()['getVisibility()'] == 'VISIBLE':
			return True
		
		return False     
	
#-----------------------------------------------------------------------------# 

class EmulatorKeyword(Keyword):
	
	def sendCommand(self, command):
		print command
		
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect( ('localhost', int(self._target.name[self._target.name.find("-") + 1:])) )
			data = sock.recv(4096)
			sock.send(command +"\n")
			data = sock.recv(4096)
			if not data.strip().endswith("OK"):
				return False
			sock.close()
			
		except socket.error,msg:
			self.log(msg)
			return False
				
		return True   

#-----------------------------------------------------------------------------#

class SetNetworkDelay(EmulatorKeyword):

	def __init__(self):
		super(SetNetworkDelay,self).__init__()
		pattern = re.compile('gprs|edge|umts|none')
		self.attributePattern = pattern
                self.shouldLog = False
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		return self.sendCommand("network delay " + matcher.group(0))

#-----------------------------------------------------------------------------#

class SetNetworkSpeed(EmulatorKeyword):

	def __init__(self):
		super(SetNetworkSpeed,self).__init__()
		pattern = re.compile('gsm|hscsd|gprs|edge|umts|hsdpa|full')
		self.attributePattern = pattern
                self.shouldLog = False
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		return self.sendCommand("network speed " + matcher.group(0))   

#-----------------------------------------------------------------------------#

class SendSMS(EmulatorKeyword):

	def __init__(self):
		super(SendSMS,self).__init__()
		pattern = re.compile("(\d+)\s*,\s*'(.*)'")
		self.attributePattern = pattern
                self.shouldLog = True
				  
	def execute(self):
	
		matcher = self.attributePattern.match(self.attributes)
		return self.sendCommand("sms send " + matcher.group(1) + " " + matcher.group(2))

#-----------------------------------------------------------------------------#
