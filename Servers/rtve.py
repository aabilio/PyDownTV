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

# Módulo para descargar todos los audios de la web de rtve.es ("A la carta" o no)

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

class RTVE(object): # Identificativo del canal
    '''
        Clase para menjera los audios de la RTVE (todos)
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
            Procesa lo necesario para obtener la url final del audio a descargar y devuelve
            esta y el nombre como se quiere que se descarge el archivo de la siguiente forma:
            return [ruta_url, nombre]

            Si no se quiere especificar un nombre para el archivo resultante en disco, o no se
            conoce un procedimiento para obtener este automáticamente se utilizará:
            return [ruta_url, None]
            Y el método de Descargar que descarga utilizará el nombre por defecto según la url.
        '''
        # Primero: nos quedamos con le id dependiendo si el user metio la url con
        # una barra (/) final o no y si tiene extensión (no es alacarta)
        audioID = self._URL_recibida.split('/')[-1]
        if audioID == "":
            audioID = self._URL_recibida.split('/')[-2]
        elif audioID.find(".shtml") != -1 or audioID.find(".html") != -1 or \
            audioID.find(".html") != -1:
            audioID = audioID.split('.')[0]
        
        
        printt(u"[INFO] ID del Audio   :", audioID)
        xmlURL = "http://www.rtve.es/swf/data/es/audios/audio/" + audioID[-1] \
                + "/" + audioID[-2] + "/" + audioID[-3] \
                + "/" + audioID[-4] + "/" + audioID + ".xml"
        printt(u"[INFO] Url de xml     :", xmlURL)
        #print "[+] Procesando Descarga"

        sourceXML = self.__descXML(xmlURL)
        
        # Ahora la url final del audio puede estar entre las etiquetas <file></file>
        # o puede que tengamos que dar un rodeo
        if sourceXML.find("<file>") != -1 and sourceXML.find("</file>"): # Contiene la URL
            urlAudio = sourceXML.split("<file>")[1].split("</file>")[0]
        elif sourceXML.find("assetDataId::") != -1: # Dar el rodeo
            idAsset = sourceXML.split("assetDataId::")[1].split("\"/>")[0]
            printt(u"[INFO] Nuevo ID Asset :",  idAsset)
            urlXMLasset = "www.rtve.es/scd/CONTENTS/ASSET_DATA_AUDIO/" + idAsset[-1] \
                        + "/" + idAsset[-2] + "/" + idAsset[-3] \
                        + "/" + idAsset[-4] + "/ASSET_DATA_AUDIO-" + idAsset + ".xml"
            printt(u"[INFO] XML URL Asset  :",  urlXMLasset)
            sourceAssetXML = self.__descXML(urlXMLasset)
            urlInSourceAssetXML = sourceAssetXML.split("defaultLocation=\"")[1].split("\"")[0]
            #print "urllInSourceAssetXML =", urlInSourceAssetXML
            urlAudio = "http://www.rtve.es/resources/TE_NGVA/mp3/" + urlInSourceAssetXML.split("/mp3/")[1]
        else:
            salir(u"[!!!] No se encuentró la URL del Audio")
        
        

        # Nombre con el que se guardará la descarga:
        extension = '.' + urlAudio.split('.')[-1]
        name =  sourceXML.split("<name>")[1].split("</name")[0] + extension
        name = formatearNombre(name)

        return [urlAudio, name]
