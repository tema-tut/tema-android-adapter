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

"""
Module for running keyword-driven tests in Android

"""

import subprocess
import time

# from adapterlib.ToolProtocol import *
# from adapterlib.ToolProtocolHTTP import *
from adapterlib.testrunner import TestRunner,Target
# import adapterlib.keyword as keyword

import AndroidAdapter.monkeydriver as monkeydriver
import AndroidAdapter.guireader as guireader
from AndroidAdapter.ui_keywords import *

class AndroidTarget(Target):
    
    def __init__(self,name,monkey_port, window_port):
        Target.__init__(self,name)
        self.__monkey_port = monkey_port
        self.__window_port = window_port

    def cleanup(self):
        pass
    
    def setup(self):
    
        self.__monkeydriver = monkeydriver.MonkeyDriver(port = self.__monkey_port)
        self.__guireader = guireader.GuiReader(self.name, self.__monkeydriver, port = self.__window_port)
        
        commands = ["shell service call window 1 i32 4939",
                        "forward tcp:" + str(self.__window_port) + " tcp:4939",
                        "forward tcp:" + str(self.__monkey_port) + " tcp:1080"]
            
        for c in commands:
        
            retcode = subprocess.call("adb -s " + self.name + " " + c,shell = True, stdout = subprocess.PIPE )
            
            if retcode != 0:
                print "Error when intializating testing environment, make sure android sdk tools are in the path and the SUT is specified"
                return False
        
        try:
            p = subprocess.Popen("adb -s " + self.name + " shell monkey --port 1080",shell = True, stdout = subprocess.PIPE)
            print "connecting monkey application . . .",
            while True:
                print ".",
                if self.__monkeydriver.connectMonkey():
                    x,y = self.__monkeydriver.getScreenSize()
                else:
                    print "Can't connect to monkey application."
                    return False

                if x != None and y != None:
                    print "connected"
                    break
                else:
                    time.sleep(1)

       
        except OSError:
            print "Error launching Monkey application"
            return False
        
        return True
    
    def takeScreenShot(self,path):
        self.__guireader.takeScreenshot(path)
        return True
    
    def getGUIReader(self):
        return self.__guireader
    
    def getMonkeyDriver(self):
        return self.__monkeydriver


class AndroidSystemTestRunner(TestRunner):


    def __init__(self, targets, delay, record = False ):
        TestRunner.__init__(self,targets,delay,record)
        self._commands["special"].extend(["dump","screenshot"])
        self._commands["kws"] = ["list","kws"]
        self._commands["info"] = []
    
    def _cleanupTestAutomation(self):
        pass

    def _setupTestAutomation(self):
        
        w_port = 4939 
        m_port = 1080
        
        for t in self._targetNames:
            print "Initializating target: " + t
            
            target = AndroidTarget(t,m_port,w_port)
            self._targets.append(target)
            if not target.setup():
                return False
            
            w_port += 1
            m_port += 1
        return True
        
    def _handleSpecialCommands(self,command):
    
        if command == "dump":
            self._activeTarget.getGUIReader().readGUI()
            self._activeTarget.getGUIReader().printDump()
                
        elif command == "screenshot":
            print "Taking screenshot...",
            self._activeTarget.getGUIReader().takeScreenshot()
            print "done" 
    
        else:
            return False
            
        return True
