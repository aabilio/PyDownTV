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

#from ez_setup import use_setuptools
#use_setuptools()

from distutils.core import setup
#from setuptools import setup

import py2exe

setup(name="PydownTV", 
    version="3.0",
    description=u"Descarga vídeos de las webs de TVs Españolas".encode("cp850"),
    author="Abilio Almeida Eiroa",
    author_email="aabilio@gmail.com",
    url="http://code.google.com/p/pydowntv/",
    license="GPL3",
    scripts=["pydowntv.py"], 
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
                "Servers.tv3", 
                "Servers.eitb", 
                "Servers.extremadura", 
                "Servers.televigo", 
                "Servers.tvamuercia", 
                "Servers.intereconomia", 
                "Servers.giraldatv", 
                "Servers.riasbaixas", 
                "Servers.rtvcyl", 
                "Servers.utiles",
                "Servers.Descargar",
                "Servers.pyaxel.pyaxel",
                "Servers.pylibmms.core",
                "Servers.pylibmms.libmms"], 
    console=[{"script": "pydowntv.py", "icon_resources": [(1, "icon.ico")]}], 
    #console=["pydowntv.py"],
    #windows=[{"script": "pydowntv.py", "icon_resources": [(1, "icon.ico")]}], 
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None
)
    
    
