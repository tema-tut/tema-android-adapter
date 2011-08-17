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
Uses the android screenshot application to capture device screen

Screenshot is a Java-application delivered with the android source and must be
compiled and set up with the following instructions:

1. copy <androidsource>\sdk\screenshot\src\com folder to <androidsdk>\tools
2. with command line, go to <androidsdk>\tools
3. compile the code: javac -classpath lib\ddmlib.jar com\android\screenshot\Screenshot.java
4. set the sdk's tools folder and the <androidsdk>\tools\lib\ddmlib.jar to the CLASSPATH environment variable
5. You should now be able to run the application from any path with the command: java com.android.screenshot.Screenshot

"""

import subprocess

def captureScreen(out_file, serial_id):
	
	#retcode = subprocess.call("java com.android.screenshot.Screenshot " + "-s " + serial_id + "" + out_file + "",
	#	stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell=True, )
	
	retcode =  subprocess.call(["java", "com.android.screenshot.Screenshot", "-s", serial_id , out_file],stdout = subprocess.PIPE,stderr = subprocess.PIPE)

	
	if retcode != 0:
		print "Error: screenshot application not configured!"
	
if __name__ == "__main__":
	captureScreen("pic.png", "emulator-5554")
	
