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

# Pequeña descripción de qué canal de tv es el módulo

__author__="Tu nombre"
__date__ ="$31-mar-2011 23:11:07$"

# Puedes importar Descargar para utilizar su método descargar al que se le pasa una
# url y delvuelve un strema con el contenido de lo descargado:
# ejemplo:
# D = Descargar(url)
# stream = D.descargar()
from Descargar import Descargar
import sys  # Utilizo sys para llamar a sys.exit() ya que si uso exit() me da
            # Problemas en ejecución tras usar Py2exe

class Telecinco(object): # Identificativo del canal
    '''
        Descripción de la clase
    '''

    URL_DESCARGA_TELECINCO = "http://www.mitele.telecinco.es/deliverty/demo/resources/flv/"

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)
    
    def __formatearNombre(self, nombre):
        '''
            Se le pasa una cadena por parámetro y formatea esta quitándole caracteres
            que pueden colisionar a la hora de realizar el guardado en disco la descarga
        '''

        nombre = nombre.replace('/',"-") # Quitar las barras "/"
        nombre = nombre.replace(" ", "_") # Quirar espacios
        nombre = nombre.replace("_-_", "-")
        nombre = nombre.replace(". ", ".") # Punto + espacio = solo punto
        nombre = nombre.replace("&#146;", "=") # Cambiar el caracter escapado (') por (=)

        return nombre

    # Funciones privadas que ayuden a procesarDescarga(self):
    def __descHTML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar el HTML '''
        D = Descargar(url2down)
        return D.descargar()

    def procesarDescarga(self):
        '''
            Procesa lo necesario para obtener la url final del vídeo a descargar y devuelve
            esta y el nombre como se quiere que se descarge el archivo de la siguiente forma:
            return [ruta_url, nombre]

            Si no se quiere especificar un nombre para el archivo resultante en disco, o no se
            conoce un procedimiento para obtener este automáticamente se utilizará:
            return [ruta_url, None]
            Y el método de Descargar que descarga utilizará el nombre por defecto según la url.
        '''
        streamHTML = self.__descHTML(self._URL_recibida)
        videoID = streamHTML.split("\'http://level3/")[1].split("\\.")[0]
        url2down = URL_DESCARGA_TELECINCO + videoID[-1] + "/" + videoID[-2] + "/" + videoID + ".flv"

        name = None

        return [url2down, None]



