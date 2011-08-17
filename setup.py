#!/usr/bin/env python
# -*- coding: utf-8
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
from __future__ import with_statement
from distutils.core import setup
from distutils.command.build_scripts import build_scripts,first_line_re
from distutils.command.bdist_wininst import bdist_wininst
from distutils.dist import Distribution

from shutil import copyfile,rmtree
from tempfile import mkdtemp
import os

class Distribution_extended(Distribution):
    def __init__ (self, attrs=None):
        self.add_prefix = False
        self.remove_prefix = False
        Distribution.__init__(self,attrs)

class bdist_wininst_extended(bdist_wininst):
    def run(self):
        self.distribution.add_prefix = True
        bdist_wininst.run(self)
        
class build_scripts_add_extension(build_scripts):

    def _transform_script_name(self,script_name):
        script_base = os.path.basename(script_name)
        filu = open(script_name,'r')
        firstline = filu.readline()
        filu.close()
        if firstline:
            match = first_line_re.match(firstline)
        else:
            match = None
                    
        file_name = script_base
        if match:
            if self.distribution.add_prefix and not script_base.endswith(".py"):
                file_name = "%s.py" % script_base
            if self.distribution.remove_prefix and script_base.endswith(".py"):
                file_name = script_base[:-3]


        if not file_name.startswith("tema."):
            file_name = "tema.%s" % file_name

        return file_name

    def run(self):
        # Not in posix system. Add prefix .py just to be sure
        if os.name != "posix":
            self.distribution.add_prefix = True
        # Remove .py prefix in posix. 
        elif os.name == "posix" and not self.distribution.add_prefix:
            self.distribution.remove_prefix = True

        try:
            tempdir = mkdtemp()
            new_names = []
            for script in self.scripts:
                new_name = os.path.join(tempdir,self._transform_script_name(script))
                new_names.append(new_name)
                copyfile(script,new_name)

            self.scripts = new_names
            build_scripts.run(self)
        finally:
            if os.path.isdir(tempdir):
                rmtree(tempdir)


with open("LICENCE",'r') as input_h:
    LICENCE=input_h.read()

VERSION="3.2"

setup(name='tema-android-adapter',
      provides=['AndroidAdapter',],
      requires=['adapterlib',],
      license=LICENCE,
      version=VERSION,
      description='Android Adapter for TEMA Tools',
      long_description='Android Adapter for TEMA Tools. Android Adapter is used to run automatic keyword-based tests on Android GUI. Requires Android SDK.',
      author="Tampere University of Technology, Department of Software Systems",
      author_email='teams@cs.tut.fi',
      url='http://tema.cs.tut.fi',
      packages=['AndroidAdapter'],
      scripts=['tema.android-adapter'],
      data_files=[('share/man/man1', ['tema.android-adapter.1'])],
      cmdclass={"build_scripts"  : build_scripts_add_extension, "bdist_wininst" : bdist_wininst_extended },
      distclass=Distribution_extended,
     )
