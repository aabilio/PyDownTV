#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyDownTV.
#
#    PyDownTV is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyDownTV is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyDownTV.  If not, see <http://www.gnu.org/licenses/>.

# Archivo setup.py del proyecto PyDownTV:

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

import py2app

setup(name="PydownTV", 
    version="2.5",
    description="Descarga vídeos de las webs de TVs Españolas",
    author="Abilio Almeida Eiroa",
    author_email="aabilio@gmail.com",
    url="http://code.google.com/p/pydowntv/",
    license="GPL3",
    scripts=["pydowntv.py"],
    app=["pydowntv.py"],
    packages = ["Servers",
                "Servers.pyaxel",
                "Servers.pylibmms"], 
    py_modules=["Servers.tve",
                "Servers.rtve",
                "Servers.a3",
                "Servers.telecinco",
                "Servers.crtvg",
                "Servers.btv", 
                "Servers.canalsur", 
                "Servers.rtvv", 
                "Servers.utiles",
                "Servers.Descargar",
                "Servers.pyaxel.pyaxel",
                "Servers.pylibmms.core",
                "Servers.pylibmms.libmms"], 
    options={'py2app': {'argv_emulation': False}},
    setup_requires=['py2app'],
)
    
    
