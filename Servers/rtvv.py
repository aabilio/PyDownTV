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

__author__="aabilo"
__date__ ="$06-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys 

class RTVV(object): 
    '''
        Descripción de la clase que maneja las descargas de Ràdio Televisió Valenciana
    '''
    
    URL_RTVV = "http://www.rtvv.es"

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
        
    def __getHtmlUrlFromAlacarta(self):
        '''
            Dada una URL de A la Carta de RTVV devuelve su URL normal
        '''
        id = self._URL_recibida.split("/")[-1]
        if id.find("#") == -1 or self._URL_recibida.endswith("rtvv.es/va/noualacarta/") or \
                                        self._URL_recibida.endswith("rtvv.es/va/noualacarta"):
            salir(u"[ERROR] Página general de \"A la Carta\". Introducir url específica")
        id = id.replace("#", "")
        printt(u"[INFO] ID:", id)
        frameIDsplit = "<li class=\"scr-item contentId_" + id + "\">"
        printt(u"[INFO] Separador:", frameIDsplit)
        frameID = self.__descHTML(self._URL_recibida).split(frameIDsplit)[1].split("</li>")[0]
        htmlURL = self.URL_RTVV + frameID.split("<a href=\"")[1].split("\"")[0]
        
        return htmlURL
    
    def __rtvvRadio(self, htmlStream, sep):
        '''
            Dada una URL de la radio de RTVV devuelve la URL y el NOMBRE de descarga del audio
        '''
        printt(u"[INFO] Modo Audios de Ràdio")
        url = self.URL_RTVV + htmlStream.split(sep)[1].split("\"")[0]
        ext = "." + url.split(".")[-1]
        name = htmlStream.split("class=\"title\"><strong>")[1].split("<")[0] + ext
        
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
        # Comprobar si es de radio primero:
        firstHtmlCheck = self.__descHTML(self._URL_recibida)
        separador = "this.element.jPlayer(\"setFile\", \""
        if firstHtmlCheck.find(separador) != -1 and firstHtmlCheck.find(".mp3") != -1:
            url, name = self.__rtvvRadio(firstHtmlCheck, separador)
            if name:
                name = formatearNombre(name)
            return [url, name]
        # FIN Ràdio
        
        # Ahora Vídeos
        if self._URL_recibida.find("rtvv.es/va/noualacarta") != -1:
            printt(u"[INFO] A la Carta")
            xmlURL = self.URL_RTVV + self.__descHTML(self.__getHtmlUrlFromAlacarta()).split("file: \"")[1].split("\"")[0]
        else:
            printt(u"[INFO] Vídeo Normal")
            xmlURL = self.URL_RTVV + self.__descHTML(self._URL_recibida).split("file: \"")[1].split("\"")[0]
            
        printt(u"[INFO] URL de XML:", xmlURL)
        xmlStream = self.__descHTML(xmlURL)
        url = xmlStream.split("<media:content url=\"")[1].split("\"")[0]
        ext = "." + url.split(".")[-1]
        # Acotar a <item></item> para coger el <title> del <item>
        item = xmlStream.split("<item>")[1].split("</item>")[0]
        name = item.split("<title><![CDATA[")[1].split("]")[0] + ext
        
        if name:
            name = formatearNombre(name)

        return [url, name]



