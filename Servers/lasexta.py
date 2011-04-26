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

# Módulo para manejar los vídeos de la web de La Sexta

__author__="aabilio"
__date__ ="$07-abr-2011 11:03:38$"

# Puedes importar Descargar para utilizar su método descargar al que se le pasa una
# url y delvuelve un strema con el contenido de lo descargado:
# ejemplo:
# D = Descargar(url)
# stream = D.descargar()
from Descargar import Descargar
from utiles import salir, formatearNombre
import sys  # Utilizo sys para llamar a sys.exit() ya que si uso exit() me da
            # Problemas en ejecución tras usar Py2exe

class LaSexta(object): # Identificativo del canal
    '''
        Clase para manejar los videos de la página web de La Sexta
    '''

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)
    
    # Funciones privadas que ayuden a procesarDescarga(self):

    def procesarDescarga(self):
        '''
            Procesa lo necesario para obtener la url final del vídeo a descargar y devuelve
            esta y el nombre como se quiere que se descarge el archivo de la siguiente forma:
            return [ruta_url, nombre]

            Si no se quiere especificar un nombre para el archivo resultante en disco, o no se
            conoce un procedimiento para obtener este automáticamente se utilizará:
            return [ruta_url, None]
            Y el método de Descargar que descarga utilizará el nombre por defecto según la url.
            
            Tanto "ruta_url" como "nombre" pueden ser listas (por supuesto, el nombre del ruta_url[0]
            tiene que ser nombre[0] y así sucesivamente).
        '''

        # Esta es realmente la parte importante, la que procesa lo necesario para obtener la url
        # final de descarga del vídeo.

        return [url, None]



