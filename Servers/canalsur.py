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
__date__ ="$06-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys 

class CSur(object):
    '''
        Descripción de la clase CSur que maneja lo descarga de los vídeos de Canal Sur
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
        
    def __alacarta(self):
        '''return URL y NAME de los vídeos de A la carta de Canal SUR'''
        printt(u"[INFO] A la carta")
        xmlStream = self.__descHTML(self.__descHTML(self._URL_recibida).split("_url_xml_datos=")[1].split("\"")[0])
        url = xmlStream.split("<url>")[1].split("<")[0]
        ext = "." + url.split(".")[-1]
        name = xmlStream.split("<title><![CDATA[")[1].split("]")[0] + ext
        
        return [url, name]
        
        
    def __modoNormal(self):
        '''return URL y NAME de los vídeos normales de Canal SUR'''
        printt(u"[INFO] Vídeo Normal")
        htmlStream = self.__descHTML(self._URL_recibida)
        url = "http://www.canalsur.es" + htmlStream.split("flashvars=\"file=")[1].split("&")[0]
        ext = "." + url.split(".")[-1]
        name = htmlStream.split("<title>")[1].split("<")[0] + ext
        
        return [url, name]

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
        
        if self._URL_recibida.find("canalsuralacarta.es") != -1: # CSur a la carta:
            url, name = self.__alacarta()
        elif self._URL_recibida.find("canalsur.es/") != -1: # Vídeos normales
            url, name = self.__modoNormal()
        else: # No debería de suceder nuca
            salir(u"[!!!] Error inesperado")

        if name:
            name = formatearNombre(name)

        return [url, name]



