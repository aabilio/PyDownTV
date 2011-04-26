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

# Se establece la Clase del objeto a3: que maneja los métodos para descargar
# los vídeos de la página de Antena 3 Televisón:

__author__="aabilio"
__date__ ="$29-mar-2011 11:03:38$"

import sys
from Descargar import Descargar
from utiles import salir, formatearNombre

class A3(object):
    '''
        Clase de de A3 que maneja los métodos para descargar los vídeos de
        la web de antena3.com
    '''
    URL_DE_ANTENA3  = "http://antena3.com/"
    URL_DE_DESCARGA = "http://desprogresiva.antena3.com/"

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)

    def __descHTML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar el HTML '''
        D = Descargar(url2down)
        return D.descargar()
    def __descXML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar HTML '''
        D = Descargar(url2down)
        return D.descargar()

    def __modoSalon(self, streamHTML):
        print "[INFO] Modo Salón"
        streamXML = \
        self.__descXML(self.URL_DE_ANTENA3 + streamHTML.split("player_capitulo.xml='")[1].split("'")[0])
        url2down = self.URL_DE_DESCARGA + \
            streamXML.split("<archivo><![CDATA[")[1].split("001.mp4]]></archivo>")[0] + "000.mp4"
        name = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0] + ".mp4"
        
        return [url2down,  name]
    def __modoNormalConURL(self,  streamHTML):
        url2down = streamHTML.split(".seoURL='")[1].split("'")[0]
        name = self.__descXML(self.URL_DE_ANTENA3 + streamHTML.split(".xml='")[1].split("'")[0]).split("<nombre><![CDATA[")[1].split("]]>")[0] + ".mp4"
                
        return [url2down,  name]
    def __modoNormalVariasPartes(self, streamHTML):
        url2down = []
        name = []
        # Delimitamos la parte del carrusel (funcionará para todos??)
        streamHTML = streamHTML.split("<a title=\"Video Anterior\"")[1].split("<a title=\"Video Siguiente\"")[0]
        partes = len(streamHTML.split("<img title="))-1
        streamPARTES = streamHTML.split("<img title=")[1:]
        print "[INFO] Número de partes:", partes
        #print streamPARTES
        for i in streamPARTES:
            xmlURL = self.URL_DE_ANTENA3 + i.split("rel=\"/")[1].split("\"")[0]
            streamXML = self.__descXML(xmlURL)
            url2down.append(self.URL_DE_DESCARGA + streamXML.split("<archivo><![CDATA[")[1].split("]")[0])
            name.append(i.split("\"")[1].split("\"")[0])
        
        print "[INFO] URLs    :",  url2down
        print "[INFO] Nombres :",  name
        
        return [url2down, name]
    def __modoNormalUnaParte(self, streamHTML):
        xmlURL = streamHTML.split("A3Player.swf?xml=")[1].split("\"")[0]
        streamXML = self.__descXML(xmlURL)
        url2down =  self.URL_DE_DESCARGA + \
        streamXML.split("<archivo><![CDATA[")[1].split("]]></archivo>")[0]
        name = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0] + ".mp4"
        
        return [url2down, name]
    
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
        # print "[+] Procesando descarga"
        streamHTML = self.__descHTML(self._URL_recibida)
        if self._URL_recibida.find("antena3.com/videos/") != -1: # Modo Salón
            url2down,  name = self.__modoSalon(streamHTML)
        else: # Otro vídeos (No modo salón)
            print "[INFO] Vídeo normal"
            if streamHTML.find(".seoURL='") != -1: # Url directamente en HTML
                url2down, name = self.__modoNormalConURL(streamHTML)
            else: # No está la url en el hmtl (buscar por varias partes)
                if streamHTML.find("<div class=\"visor\">") != -1: # Más de 1 parte # Quizas mejor "carrusel"?
                    url2down, name = self.__modoNormalVariasPartes(streamHTML)
                else: # Solo una parte
                    url2down, name = self.__modoNormalUnaParte(streamHTML)
        
        if type(url2down) == list:
            for i in url2down:
                if i.find("geobloqueo") != -1:
                    print "[!!!] El vídeo \"" + i + "\" no se puedo descargar (geobloqueado)"
                    url2down.remove(i)
                    # TODO: Borrar también su nombre correspondiente
                
            # Comprobar si todas las partes están geobloqueadas (no quedan elementos en la lista):
            if len(url2down) == 0:
                salir("[!] No se puede descargar ninguna parte (geobloqueadas)")
        else:
            if url2down.find("geobloqueo") != -1:
                salir("[!] El vídeo no se puede descargar (geobloqueado)")

        if type(name) == list:
            for i in name:
                b = formatearNombre(i)
                name[name.index(i)] = b
        else:
            name = formatearNombre(name)
        
        return [url2down , name]

