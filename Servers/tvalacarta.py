#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DEPRECATED 
# (se usa el módulo de tve.py para descargar estos vídeos también)

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

__author__="aabilio"
__date__ ="$31-mar-2011 11:35:37$"

# Puedes importar Descargar para utilizar su método descargar al que se le pasa una
# url y delvuelve un strema con el contenido de lo descargado:
# ejemplo:
# D = Descargar(url)
# stream = D.descargar()

import sys
from Descargar import Descargar
from utiles import salir, formatearNombre, printt

class TvAlacarta(object): # Identificativo del canal
    '''
        Clase para menjera los vídeos de la RTVE, de la sección:
        Televisión a la carta.
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
        # Primero: nos quedamos con le id dependiendo si el user metio la url con
        # una barra (/) final o no y si tiene extensión (no es alacarta)
        videoID = self._URL_recibida.split('/')[-1]
        if videoID == "":
            videoID = self._URL_recibida.split('/')[-2]
        elif videoID.find(".shtml") != -1 or videoID.find(".html") != -1 or \
            videoID.find(".html") != -1:
            videoID = videoID.split('.')[0]
        
        
        printt(u"[INFO] ID del Vídeo :", videoID)
        xmlURL = "www.rtve.es/swf/data/es/videos/video/" + videoID[-1] \
                + "/" + videoID[-2] + "/" + videoID[-3] \
                + "/" + videoID[-4] + "/" + videoID + ".xml"
        printt(u"[INFO] Url de xml   :", xmlURL)
        #print "[+] Procesando Descarga"

        sourceXML = self.__descXML(xmlURL)
        if sourceXML == -1:    # Comprobar si existe (No es tve a la carta)
            sourceHTML = self.__descHTML(self._URL_recibida)
            if sourceHTML.find("<div id=\"video") != -1:
                id = sourceHTML.split("<div id=\"video")[1].split("\"")[0]
            elif sourceHTML.find("<div id=\"vid") != -1:
                id = sourceHTML.split("<div id=\"vid")[1].split("\"")[0]
            else:
                salir(u"[!] ERROR al generear el nuevo id")
            xmlURL = "www.rtve.es/swf/data/es/videos/video/" + id[-1] \
                + "/" + id[-2] + "/" + id[-3] \
                + "/" + id[-4] + "/" + id + ".xml"
            sourceXML = self.__descXML(xmlURL)
            printt(u"[INFO] Nuevo vídeo ID:",  id)
            printt(u"[INFO] Nuevo url de xml:", xmlURL) 
            

        # Ahora la url final del video puede estar entre las etiquetas <file></file>
        # o puede que tengamos que dar un rodeo
        if sourceXML.find("<file>") != -1 and sourceXML.find("</file>"): # Contiene la URL
            urlVideo = sourceXML.split("<file>")[1].split("</file>")[0]
        elif sourceXML.find("assetDataId::") != -1: # Dar el rodeo
            idAsset = sourceXML.split("assetDataId::")[1].split("\"/>")[0]
            urlXMLasset = "www.rtve.es/scd/CONTENTS/ASSET_DATA_VIDEO/" + idAsset[-1] \
                        + "/" + idAsset[-2] + "/" + idAsset[-3] \
                        + "/" + idAsset[-4] + "/ASSET_DATA_VIDEO-" + idAsset + ".xml"
            sourceAssetXML = self.__descXML(urlXMLasset)
            urlInSourceAssetXML = sourceAssetXML.split("defaultLocation=\"")[1].split("\"")[0]
            #print "urllInSourceAssetXML =", urlInSourceAssetXML

            # Es flv o mp4?
            if urlInSourceAssetXML.find("/flv/") != -1:
                urlVideo = "http://www.rtve.es/resources/TE_NGVA/flv/" \
                        + urlInSourceAssetXML.split("/flv/")[1]
            elif urlInSourceAssetXML.find("/mp4/") != -1:
                urlVideo = "http://www.rtve.es/resources/TE_NGVA/mp4/" \
                        + urlInSourceAssetXML.split("/mp4/")[1]
            else:
                salir(u"Vídeo no encontrado")
            
            
        else:
            salir(u"No se encuentra la URL del vídeo")

        # Nombre con el que se guardará la descarga:
        extension = '.' + urlVideo.split('.')[-1]
        name =  sourceXML.split("<name>")[1].split("</name")[0] + extension
        name = formatearNombre(name)

        return [urlVideo, name]



