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
__date__ ="$19-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys  

class RTVCM(object):
    '''
        Clase que maneja la descarga los vídeos de RTVCM
    '''
    
    URL_RTVCM = "http://www.rtvcm.es"
    URL_MULTIMEDIA = "http://www.rtvcm.es/mm.php?id="
    
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
        
    def __paginaDvideo(self, streamHTML, nuevoID=None, name=None):
        '''return url & name si la página que se pasa es directamente la del vídeo'''
        if nuevoID is None and name is None:
            nStreamHTML = streamHTML.replace(" ", "")
        else:
            nStreamHTML = self.__descHTML(self.URL_MULTIMEDIA + nuevoID).replace(" ", "")
            
        url = nStreamHTML.split("data=\"")[1].split("\"")[0]
        if name is None:
            name = url.split("/")[-1]
            
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
        
        streamHTML = self.__descHTML(self._URL_recibida)
        if self._URL_recibida.find("detail.php?id") != -1: # Aun no es el vídeo
            if streamHTML.find("ShowPreviewMM(\'") != -1:
                url = streamHTML.split("ShowPreviewMM(\'")[1].split("\'")[0]
                name = streamHTML.split("); return false;\">")[1].split("<")[0]
            elif streamHTML.find("onClick=\"ShowPreviewMM(") != -1:
                printt(u"[INFO] Buscando ID del vídeo")
                nuevoID = streamHTML.split("onClick=\"ShowPreviewMM(")[1].split(")")[0]
                printt(u"[INFO] Vídeo ID:", nuevoID)
                name = streamHTML.split("); return false;\">")[1].split("<")[0]
                url, name = self.__paginaDvideo(streamHTML, nuevoID, name)
            else:
                salir(u"[!!!] No se reconoce el tipo de contenido")
        elif self._URL_recibida.find("mm.php?id") != -1:
            url, name = self.__paginaDvideo(streamHTML)
        elif streamHTML.find("youtube"):
            salir(u"[!!!] No se reconoce el tipo de contenido.\nPuede que el vídeo sea de YouTube??")
        else:
            salir(u"[!!!] No se reconoce el tipo de contenido")
        
        url = url.replace("http://", "mms://")
        ext = "." + url.split(".")[-1]
        if name.find(ext) == -1:
            name += ext.lower()
        
        if name:
            name = formatearNombre(name)

        return [url, name]



