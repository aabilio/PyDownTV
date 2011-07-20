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

# Módulo para manejar los vídeos de la web de La Sexta

__author__="aabilio"
__date__ ="$07-abr-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys
from pprint import pprint

class LaSexta(object): 
    '''
        Clase para manejar los videos de la página web de La Sexta
    '''

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)
    
    # Funciones privadas que ayuden a procesarDescarga(self):
    
    def __GetStream(self, size):
        s = [115, 225, 72, 132, 17, 87, 200, 57, 214, 47, 221, 113, 240, 130, 237, 81, 117, 236, 114, 212, 128, 210, 226, 41, 246, 100, 178, 59, 91, 106, 199, 92, 39, 173, 145, 133, 13, 67, 124, 76, 136, 102, 172, 77, 230, 7, 123, 245, 42, 239, 5, 186, 189, 11, 249, 170, 75, 182, 174, 34, 216, 82, 243, 165, 167, 104, 228, 70, 94, 191, 204, 234, 244, 55, 127, 218, 31, 184, 201, 120, 135, 206, 190, 222, 160, 171, 205, 36, 18, 169, 80, 95, 168, 46, 161, 177, 166, 52, 54, 56, 119, 126, 143, 79, 224, 116, 121, 241, 35, 242, 28, 122, 196, 140, 129, 2, 220, 43, 208, 16, 192, 30, 53, 118, 176, 153, 97, 252, 139, 253, 101, 112, 232, 58, 188, 1, 19, 131, 238, 61, 88, 229, 108, 24, 179, 109, 33, 69, 255, 250, 149, 40, 20, 98, 144, 194, 209, 193, 164, 74, 105, 227, 195, 158, 180, 51, 163, 45, 10, 23, 93, 89, 110, 60, 3, 187, 125, 99, 134, 254, 197, 29, 147, 9, 141, 96, 73, 157, 150, 159, 83, 86, 152, 202, 22, 142, 78, 223, 66, 84, 247, 38, 21, 12, 63, 8, 137, 4, 198, 231, 68, 65, 248, 148, 44, 50, 64, 162, 90, 25, 62, 0, 217, 207, 138, 146, 27, 32, 15, 156, 37, 185, 155, 103, 71, 6, 175, 49, 85, 183, 154, 26, 235, 215, 14, 211, 107, 151, 111, 219, 251, 213, 233, 203, 181, 48]
        i = 0
        j = 0
        stream = []
        for i in xrange(size):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            h = s[i]
            s[i] = s[j]
            s[j] = h
            stream.append(s[(s[i] + s[j]) % 256])
        return stream
    
    def __HexToBytes(self, Hex):
        Bytes = []
        for i in xrange(len(Hex) / 2):
            Bytes.append(int(Hex[i * 2: (i + 1) * 2], 16))
        return Bytes

    def __BytesToStr(self, Bytes):
        result = ""
        for byte in Bytes:
            result += chr(byte)
        return result

    def __showURL(self, ciphertext):
        ciphertext = self.__HexToBytes(ciphertext)
        stream = self.__GetStream(len(ciphertext))
        result = []
        for i in xrange(len(stream)):
            result.append(ciphertext[i] ^ stream[i])
        return self.__BytesToStr(result)
    
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
        if streamHTML.find("_urlVideo=") != -1: # Vídeo en un sola parte:
            codURL = streamHTML.split("_urlVideo=")[1].split("&")[0]
            url = self.__showURL(codURL)
            name = streamHTML.split("<title>")[1].split("<")[0]
            if url.find("?start=") != -1: ext="." + url.split("?start=")[0].split(".")[-1]
            else: ext= "." + url.split(".")[-1]
            name += ext
        elif streamHTML.find("_url_list=") != -1:
            name1 = streamHTML.split("<title>")[1].split("<")[0]
            codURL1 = streamHTML.split("_url_list=")[1].split("&")[0]
            url1 = self.__showURL(codURL1)
            streamHTML = self.__descHTML(url1)
            
            codURL2 = []
            urls =  streamHTML.strip().split("<title>")[1:]
            for i in urls:
                #name2.append(i.split("<")[0])
                codURL2.append(i.split("<url>")[1].split("<")[0])
            
            url = []
            name = []
            b = 1
            for i in codURL2:
                tmp = self.__showURL(i)
                url.append(tmp)
                
                if tmp.find("?start=") != -1: ext="." + tmp.split("?start=")[0].split(".")[-1]
                else: ext= "." + tmp.split(".")[-1]
                name.append(name1 + "_part0" + str(b) + ext)
                b += 1
            del b
        else:
            salir(u"[!!!] ERROR: No se ha encontradoel vídeo")
        
        if type(name) is list:
            for i in name:
                b = formatearNombre(i)
                name[name.index(i)] = b
        else:
            name = formatearNombre(name)
            
        return [url, name]



