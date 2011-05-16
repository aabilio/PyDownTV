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
__date__ ="$16-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys  

class GiraldaTV(object):
    '''
        Clase que maneja la descarga los vídeos de GiraldaTV
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
        
        streamHTML = self.__descHTML(self._URL_recibida)#.replace(" ", "")
        if streamHTML.find("contentArray[") != -1:
            printt(u"[INFO] Se han detectado varios vídeos en la página:")
            # Deleimitar los bloques de vídeos:
            bloques = streamHTML.split("contentArray[")[1:]
            # Delimitar en un diccionario los videos:
            videosSucio = {}
            for i in bloques:
                videosSucio[int(i.split("]")[0])] = i.split("=")[1].split(");")[0]
            # Mostrar el menú en pantalla:
            for i in videosSucio:
                printt("\t[%4d] %s" % ( i, videosSucio[i].split("\'")[1] ))
            
            # Presentar menú para elegir vídeo:
            printt(u"[-->] Introduce el número del vídeo que quieres descargar (Ctrl+C para cancelar): ")
            while True:
                try:
                    ID = int(raw_input())
                except ValueError:
                    printt(u"[!!!] Parece que no has introducido un número. Prueba otra vez:")
                    continue
                except KeyboardInterrupt:
                    salir(u"\nBye!")
                    
                if ID < 0 or ID > len(videosSucio)-1:
                    printt(u"[!!!] No existe el vídeo con número [%4d] Prueba otra vez:" % ID)
                    continue
                else:
                    break
            
            # Consguir el vídeo según el ID:
            url = videosSucio[ID].split("\'")[7]
            ext = "." + url.split(".")[-1]
            name = videosSucio[ID].split("\'")[1] + ext
        else:
            salir(u"[!!!] ERROR: No se han econtrado vídeos en la página")
        
        if name:
            name = formatearNombre(name)

        return [url, name]



