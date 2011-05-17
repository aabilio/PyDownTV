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

# Módulo que manera la clase de Cuatro

__author__="aabilio"
__date__ ="$18-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys  

class RTVCYL(object):
    '''
        Clase que maneja las descargas de los vídeos de Radio TV de Castilla y León
    '''
    
    URL_STREAMS_START = "http://api.promecal.webtv.flumotion.com/videos/"
    URL_STREAMS_END = "/streams"
    
    URL_CUATRO = "http://www.rtvcyl.es/"

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
        
        if streamHTML.find("&videoId=") != -1:
            videoID = streamHTML.split("&videoId=")[1].split("\'")[0]
            printt(u"[INFO] Video ID:", videoID)
            streamStreams = self.__descHTML(self.URL_STREAMS_START + videoID + self.URL_STREAMS_END)
            streamStreams = streamStreams.replace(" ", "").replace("\n", "")
            videos = streamStreams.split("{")[1:]
            printt(u"[INFO] Se han detectado varios tipos de calidad:")
            b = 0
            for i in videos:
                printt(u"\t[%4d] %s" % (b, i.split("\"quality\":\"")[1].split("\"")[0]))
                b += 1
            # Presentar menú para elegir vídeo:
            printt(u"[-->] Introduce el número del tipo vídeo que quieres descargar (Ctrl+C para cancelar): ")
            while True:
                try:
                    ID = int(raw_input())
                except ValueError:
                    printt(u"[!!!] Parece que no has introducido un número. Prueba otra vez:")
                    continue
                except KeyboardInterrupt:
                    salir(u"\nBye!")
                    
                if ID < 0 or ID > len(videos)-1:
                    printt(u"[!!!] No existe el vídeo con número [%4d] Prueba otra vez:" % ID)
                    continue
                else:
                    break
            
            url = videos[ID].split("\"url\":\"")[1].split("\"")[0]
            ext = "." + url.split("?")[0].split(".")[-1]
            name = (streamHTML.split("<title>")[1].split("<")[0]).strip()
            name += ext
        else:
            salir(u"[!!!] No se encustra ningún vídeo en la página")
            

        if name:
            name = formatearNombre(name)

        return [url, name]



