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
__date__ ="$12-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys  

class TV3(object): 
    '''
        Clase que maneja la decarga de los vídeos de TV3
    '''
    
    URL_TOKEN_START = "http://www.tv3.cat/su/tvc/tvcConditionalAccess.jsp?ID="
    URL_TOKEN_END   = "&QUALITY=H&FORMAT=MP4"

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
        
    def __3cat24(self, nuevoID=None):
        '''
            Procesa los vídeos de 3cat24 si no se le pasa un nuevo ID.
            Si se le apsa ID puede que sea de 3cat24 o un vídeo a alacarta (si el ID es de alacarta)
        '''
        id = self._URL_recibida.split("/")[-1] if nuevoID is None else nuevoID
        streamHTML = self.__descHTML(self.URL_TOKEN_START + id + self.URL_TOKEN_END)
        if streamHTML.find("<error>") != -1:
            salir(u"[!!!] Error al capturar el vídeo")
        name = streamHTML.split("<media videoname=\"")[1].split("\"")[0] + ".mp4"
        url = "rtmp://" + streamHTML.split("rtmp://")[1].split("<")[0]
        
        return [url, name]
        
    def __3alacarta(self):
        '''DEPRECATED. Se utiliza la de 3cat24 que sirve para los mismo'''
        pass
        
    def __catradio(self):
        '''Procesa los audios de catradio'''
        # Primero nos quedamos con el id
        audioID = self._URL_recibida.split("/")[4]
        printt(u"[INFO] Audio ID:", audioID)
        IDsplit = "insertNewItem(\'" + audioID + "\'"
        # Nos quedamos con su identificacion
        streamID = self.__descHTML(self._URL_recibida).split(IDsplit)[1].split(">")[0]
        name = streamID.split(",")[1] + ".mp3"
        url = "http://" + streamID.split("http://")[1].split("\'")[0]
        
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
        
        # En principio parece que tenemos 4 tipos de vídeos diferentes: A la carta video, a la carta auido, a 3cat24
        
        # 3cat24.cat:
        if self._URL_recibida.find("3cat24.cat/video/") != -1:
            printt(u"[INFO] Vídeos de 3cat24")
            url, name = self.__3cat24()
            
        elif self._URL_recibida.find("3cat24.cat/") != -1: # de 3cat24 pero no directamente el vídeo
            printt(u"[INFO] 3cat24 (otros vídeos)")
            streamHTML = self.__descHTML(self._URL_recibida)
            videoID = streamHTML.split("flashvars.videoid =")[1].split(";")[0].strip()
            url, name = self.__3cat24(nuevoID=videoID)
            
        elif self._URL_recibida.find("tv3.cat/3alacarta") != -1: # Sirve la misma función de 3cat24 (con nuevoID)
            printt(u"[INFO] Vídeos de 3alacarta")
            videoID = self._URL_recibida.split("/")[-1]
            url, name = self.__3cat24(nuevoID=videoID)
        elif self._URL_recibida.find("") != -1:
            printt(u"[INFO] Audios de catradio")
            url, name = self.__catradio()
        
        if name:
            name = formatearNombre(name)

        return [url, name]



