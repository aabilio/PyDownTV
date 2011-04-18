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

__author__="aabilio"
__date__ ="$07-abr-2011 23:11:07$"

# Puedes importar Descargar para utilizar su método descargar al que se le pasa una
# url y delvuelve un strema con el contenido de lo descargado:
# ejemplo:
# D = Descargar(url)
# stream = D.descargar()
from Descargar import Descargar
from utiles import salir, formatearNombre
import sys  # Utilizo sys para llamar a sys.exit() ya que si uso exit() me da
            # Problemas en ejecución tras usar Py2exe

class Telecinco(object):
    '''
        Descripción de la clase
    '''

    URL_DESCARGA_TELECINCO = "http://www.mitele.telecinco.es/deliverty/demo/resources/flv/"
    URL_ASK4TOKEN = "http://www.mitele.telecinco.es/services/tk.php?provider=level3&protohash=/CDN/videos/"
    string2split4id = ["xmlVideo: 'http://estaticos.telecinco.es/xml/Video/Video_", "\'"]

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
        '''
        
        streamHTML = self.__descHTML(self._URL_recibida)
        
        if streamHTML.find("http://level3/") != -1: # Método antiguo
            print "[INFO] Método antiguo (mitele)"
            videoID = streamHTML.split("\'http://level3/")[1].split(".")[0]
            videoEXT = streamHTML.split("\'http://level3/")[1].split("\'")[0].split(".")[1]
            videoEXT = "." + videoEXT
            url2down = self.URL_DESCARGA_TELECINCO + videoID[-1] + "/" + videoID[-2] + "/" + videoID + videoEXT
            name = None
        elif streamHTML.find(self.string2split4id[0]) != -1: # Método nuevo
            newID = streamHTML.split(self.string2split4id[0])[1].split(self.string2split4id[1])[0].split(".")[0]
            print "[INFO] Nuevo Video ID:", newID
            ask4token = self.URL_ASK4TOKEN + newID[-3:] + "/" + newID + ".mp4"
            print "[+] Pidiendo nuevo token"
            url2down = self.__descHTML(ask4token)
            name = streamHTML.split("var title = \'")[1].split("\'")[0] + ".mp4"
        elif self._URL_recibida.find("videoURL="): # Forma con el ID en la URL (nueva??)
            videoID = self._URL_recibida.split("videoURL=")[1]
            ask4token = self.URL_ASK4TOKEN + videoID[-3:] + "/" + videoID + ".mp4"
            print "[+] Pidiendo nuevo token"
            url2down = self.__descHTML(ask4token)
            # Obtner nombre:
            xmlURL = "http://estaticos.telecinco.es/xml/Video/Video_" + videoID + ".xml"
            streamXML = self.__descHTML(xmlURL)
            name = streamXML.split("<![CDATA[")[1].split("]")[0] + ".mp4"
        else:
            salir("[!!!] No se encuentra URL de descarga")

        
        if name != None:
            name = self.formatearNombre(name)
        
        return [url2down, name]



