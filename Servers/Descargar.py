#!/usr/bin/python
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

# Clase que se encarga de descargar:

__author__="aabilio"
__date__ ="$30-mar-2011 20:57:46$"

import urllib2
import urllib
import sys

from pyaxel import pyaxel
from utiles import salir

class Descargar(object):
    ''' Clase que se encarga de descargar con urllib2 '''

    def __init__(self, url=None):
        self._outputName = None
        self._URL = url
        if self._URL == None:
            salir("ERROR: No se puede descargar la url")
    
    def getOutputName(self):
        return self._outputName
    def setOutputName(self, name):
        self._outputName = name
    
    outputName = property(getOutputName, setOutputName)

    def descargar(self):
        '''
            Recoge una url la descarga y lo devuelve
            Pensado para descargar streams HTML y XML
        '''

        if self._URL.find("http://") == -1:
            self._URL = "http://" + self._URL

        try:
            f = urllib2.urlopen(self._URL)
            stream = f.read()
            f.close()
            return stream
        except:
            if self._URL.find("rtve.es") != -1: #No salir (para identificar si es a la carta o no)
                return -1
            else:
                salir("ERROR al descargar!")
        else:
            pass

    def descargarVideo(self):
        '''
            Procesa la descarga del vídeo llamanda a la función download de pyaxel
        '''
        print ""
        print "DESCARGAR:"
        print "----------------------------------------------------------------"
        if type(self._URL) == list:
            b=1
            for i in self._URL:
                print "[ URL DE DESCARGA FINAL ] [Parte %d] %s" % (b, i)
                b += 1
        else:
            print "[ URL DE DESCARGA FINAL ]", self._URL
        
        print "[INFO] Presiona \"Ctrl + C\" para cancelar"
        print ""
        if type(self._URL) == list:
            for i in range(0, len(self._URL)):
                print "[Descargando %d parte]" % (int(i) + 1)
                options = {"output_file": self._outputName[i], "verbose": True, "max_speed": None, "num_connections": 4}
                pyaxel.download(self._URL[i], options)
                if i < len(self._URL)-1: 
                    print "=================================="
                    print ""
                    print "Parte descargada o cancelanda"
                    print "Presiona [ENTER] para continuar"
                    print "Presiona[Ctrl + C] para Cancelar"
                    print ""
                    print "=================================="
                    try:
                        raw_input()
                    except KeyboardInterrupt:
                        salir("\nBye!")
            #for (i, b) in (self._URL, self._outputName):
            #    options = {"output_file": b, "verbose": True, "max_speed": None, "num_connections": 4}
            #    pyaxel.download(i, options)
        else:
            options = {"output_file": self._outputName, "verbose": True, "max_speed": None, "num_connections": 4}
            pyaxel.download(self._URL, options)

        
