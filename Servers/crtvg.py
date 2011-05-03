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

# Pequeña descripción de qué canal de tv es el módulo

__author__="aabilio"
__date__ ="$03-may-2011 11:17:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys

class CRTVG(object): # Identificativo del canal
    '''
        Descripción de la clase
    '''

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)

    # Funciones privadas que ayuden a procesarDescarga(self):
    def __descHTML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar el HTML '''
        D = Descargar(url2down)
        return D.descargar()
    def __descXML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar HTML '''
        D = Descargar(url2down)
        return D.descargar()
    
    def __aGalegaInfo(self):
        '''
            return url (mms) y nombre de los vídeos de A galega info de crtgv
        '''
        # Creo que lo más recomendable es pedir el código javascript
        # de las WWW de debajo del vídeo
        printt(u"[INFO] A galega info")
        printt(u"El vídeo que intentas descargar pertenece a la sección A galega Info")
        printt(u"Para asegurar bajar el vídeo que quieres, haz click con el ratón a las WWW")
        printt(u"que aparecen debajo del vídeo (a la izquierda).")
        printt(u"Copiar todo el contenido y pégalo aquí")
        javascript = raw_input("Pegua aquí: ")
        asxFile = javascript.split("data=\'")[1].split("\'")[0]
        asxStream = self.__descHTML(asxFile)
        
        name = asxStream.split("<title>")[1].asplit("<")[0]
        url  = asxStream.split("<ref href = \"")[1].split("\"")[0]
        return [name, url]
    
    def __aCarta(self):
        printt(u"[INFO] Á Carta (tvg)")
        urlStream = self.__descHTML(self._URL_recibida)
        asxFile = urlStream.split("<a href=\"")[1].split("\"")[0]
        asxStream = self.__descHTML(asxFile)
        
        name = asxStream.split("<TITLE>")[1].asplit("<")[0]
        url  = asxStream.split("<ENTRY><REF HREF=\"")[1].split("\"")[0]
        return [name, url]

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

        # Diferenciar entre videos a la carta y videos de agalegainfo
        if self._URL_recibida.find("agalegainfo") != -1:
            # Vídeos de agalegainfo
            url, name = self.__aGalegaInfo()
        else:
            # Aquí son todos "á carta" o tienen más tipos de vídeos??
            url, name = self.__aCarta()
        
        if name:
            name = formatearNombre(name)

        return [url, name]



