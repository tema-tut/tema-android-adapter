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
from adapterlib.ui_keyword import UIKeyword

class ObjectKeyword(UIKeyword):
                
    def __init__(self):
        super(ObjectKeyword,self).__init__()

    def __setSearchRoot(self,value):
        self.__searchroot = value
                
    def __getSearchRoot(self):
        if self.__searchroot == None:
            return self._target.getGUIReader().getRoot()
        else:
            return self.__searchroot

    searchroot = property(__getSearchRoot,__setSearchRoot)

    def __getSearchRootReference(self):
        if self.__searchroot == None:
            return "root"
        else:
            return self.__searchroot_reference

    def __setSearchRootReference(self,value):
        self.__searchroot_reference = value

    searchrootReference = property(__getSearchRootReference,__setSearchRootReference )

    def findComponentReference(self, reference, searchAll = False):
        self._target.getGUIReader().readGUI()
        return super(ObjectKeyword,self).findComponentReference(reference, searchAll )

    def searchChildren(self, searchRoot, component, roleName = None, searchOnlyFirst = False):
        """
        @type searchRoot: ViewItem
        @rtype: None or ViewItem or [ViewItem]
        """
        #If the searched component is root, just return it
        if component == "root":
            if searchRoot == self.searchroot:
                temp = []
                temp.append(searchRoot)
                return temp
            return None
                

        matcher = re.compile("(?P<partial>partial:)?'(?P<text>.*)'").match(component)
        #Search children by their text content when enclosed with single quote
        # chars
        if( matcher != None ):
                        
            return self._target.getGUIReader().findComponentWithText(matcher.group("text"),roleName,searchRoot, not searchOnlyFirst, matcher.group("partial") != None)
                        
        #Search by id
        else:
            return self._target.getGUIReader().findComponentWithId(component,roleName,searchRoot,not searchOnlyFirst)

        
    def findHierarchically(self, searchNode, component):
        """
        @type searchNode: ViewItem
        @rtype: list or None
        @return: List of ViewItems
        """
                
        names = component.split("::") 
        print ":: separated: ",
        print names
        if names == None or len(names) < 2:
            return self.searchChildren(searchNode, component)
                
        compName = names[0]
        components = self.searchChildren(searchNode, compName)
        if components == None:
            return None               
                        
        #Check the parent names
        for name in names[0:-1]:
                
            tempNodes = []
            #check if text content or name is refereced
            matcher = re.compile("'(.*)'").match(name)
                        
            if matcher:
                text = matcher.group(1)
                        
            for comp in components:
                                
                compOK = False
                if matcher:
                    if(text == comp.getProperties()['mText']):
                        compOK = True
                                                
                elif name == None or name == "" or comp.getId() == name or (name == 'root' and comp == self._target.getGUIReader().getRoot()):
                    compOK = True
                                        
                if compOK and len(comp.getChildren()) > 0:  
                    tempNodes.extend(comp.getChildren())
                                                         
            components = tempNodes

        #Check the final components names and add accepted components to a list       
        #if name is "" all children are acceptable
        if(names[-1] != ""):
            temp = components
            components = []
            #Check if final component is name or text reference
            matcher = re.compile("'(.*)'").match(names[-1])
                        
            for t in temp:
                if matcher:
                    
                    if t.getProperties().has_key('mText') and matcher.group(1) == t.getProperties()['mText']:
                            components.append(t)
                                                
                elif names[-1] == t.getId():
                        components.append(t)
                                
        return components

    def checkNodeImplementsRole(self,node,rolename):
        return node.getClassName().find(rolename) != -1
