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

# Archivo MAIN (principal) del proyecto PyDownTV:

__author__ = "aabilio"
__date__ = "$29-mar-2011 11:01:48$"

from sys import argv, exit
import re

# Ir añadiendo según se implementen
from Servers.a3 import A3
from Servers.tve import TVE
# DEPRECATED from Servers.tvalacarta import TvAlacarta
# from Servers.telecinco import Telecinco
from Servers.Descargar import Descargar

class Servidor(object):
    '''
        Contiene los métodos para identificar a que servidor pertenece la url que
        introdujo el usuario.
    '''
    def __init__(self, url=None):
        self._url = url
    def isAntena3_(self):
        if self._url.find("antena3.com") != -1:
            return True
    def isTVE_(self):
        if self._url.find("rtve.es") != -1:
            return True
    #def isTVEaLaCarta_(self): # DEPRECATED
    #    if self._url.find("rtve.es") != -1 and self._url.find("/alacarta/") != -1:
    #        return True
    def isRTVE_(self):
        if self._url.find("rtve.es") != -1 and self._url.find("/mediateca/audios/") != -1:
            return True
    def isT5_(self):
        if self._url.find("mitele.telecinco.es") != -1:
            return True
    def isLaSexta_(self):
        if self._url.find("lasexta.com/sextatv/") != -1:
            return True
    def isCuatro_(self):
        if self._url.find("play.cuatro.com/") != -1:
            return True
    # COMPLEMENTAR CON LOS DIFERENTES SERVIDORES QUE SE VAYAN SOPORTANDO
    
    isAntena3 = property(isAntena3_)
    isTVE = property(isTVE_)
    # DEPRECATED isTVEaLaCarta = property(isTVEaLaCarta_)
    isRTVE = property(isRTVE_)
    isT5 = property(isT5_)
    isLaSexta = property(isLaSexta_)
    isCuatro = property(isCuatro_)
    
def qServidor(url):
    '''
        Comprueba utlizando la clase Servidor de que servicio ha recibido la url
        y devuelve un objeto sergún el servicio que del cual se haya pasado la
        url
    '''
    # Descomentar return según se vañan añadiendo
    server = Servidor(url)
    if server.isAntena3:
        print "[INFO] Antena 3 Televisión"
        return A3(url)
    #elif server.isTVEaLaCarta: # DEPRECATED
    #    print "[INFO] TV Española \"A la carta\""
    #    return TvAlacarta(url)
    elif server.isRTVE: # Tienes que comprobarse antes que isTVE
        exit("RTVE: Todavía no implementado")
        # return RTVE(url)
        pass
    elif server.isTVE:
        #exit("TVE: Todavía no implementado")
        return TVE(url)
        pass
    elif server.isT5:
        print "[INFO] Telecinco (Mitele)"
        exit("En desarollo")
        #return Telecinco(url)
    elif server.isLaSexta:
        exit("La Sexta: Todavía no implementado")
        # return LaSexta(url)
        pass
    elif server.isCuatro:
        exit("Cuatro: Todavía no implementado")
        # return Cuatro(url)
        pass
    else:
        msgErr = "ERROR: La URL \"" + url + "\" no pertenece a ninguna Televisión"
        exit(msgErr)
    
def help(args):
    print "USO:", args[0]
    print "o   ", args[0], "<url>"
    print "(Los dos métodos aceptan varias URLs separadas por un espacio)"
    print "PyDownTV <aabilio@gmail.com>"

def compURL(url):
    p = re.compile('^http://.+\..+$', re.IGNORECASE)
    m = p.match(url)
    if m:
        return True
    else:
        return False



if __name__ == "__main__":
    # Ver si tenemos un parámetro, si no tenemos parámetro pedir la URL por 
    # entrada estándar.
    url = None
    if len(argv) >= 2:
        #exit("ERROR: Demasiados parámetros.\nFlag --help: para ayuda")
        if argv[1] == "--help" or argv[1] == "-h":
            help(argv)
            exit()
        i = ""
        url = []
        for i in argv[1:]:
            url.append(i)
        nOfUrls = len(url)
    else:
        try:
            inPut = raw_input("Introduce las URL de los vídeos (separadas por espacios): ")
            url =  inPut.split(" ")

            nOfUrls = len(url)
        except KeyboardInterrupt:
            exit("\nBye!")

    if url != None:
        # Comprobar la url y mandarla al servidor correspondiente
        while nOfUrls-1 >= 0:
            if compURL(url[nOfUrls-1]):
                # URL comprobada: http://"algo.algo"
                servidor = qServidor(url[nOfUrls-1]) # Devuelve el objeto de la clase correspondiente
            else:
                print "[!] URL incorrecta:",  url[nOfUrls-1]
                #exit("ERROR: URL mal introducida\nFlag --help: para ayuda")
            nOfUrls -= 1
    else:
        print "No has introducido la URL!"

    # Llegados a este punto tenemos la url comprobada y tenemos el objeto
    # "servidor" perteneciente a la correspondiente Clase de servers en la que estemos
    # ya establecida. Ahora utilizar los metodos para conseguir la url de descarga
    # del vídeo:
    # Se recibe la url del video y el nombre del vídeo si este existe:
    urlDeDescarga, outputName = servidor.procesarDescarga()
    D = Descargar(urlDeDescarga)
    D.outputName = outputName
    # Y Por fin se descarga el vídeo:
    D.descargarVideo()

    #print "[+] Vídeo descargado correctamente"
