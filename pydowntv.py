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

# Archivo MAIN (principal) del proyecto PyDownTV:

__author__ = "aabilio"
__date__ = "$29-mar-2011 11:01:48$"
__version__ = "1.1-BETA"

from sys import argv, exit, platform
import re

#from ui.gui import Ui_MainWindow

# Ir añadiendo según se implementen
from Servers.a3 import A3
from Servers.tve import TVE
from Servers.rtve import RTVE
# DEPRECATED from Servers.tvalacarta import TvAlacarta
from Servers.telecinco import Telecinco
# from Servers.lasexta import LaSexta
# from Servers.cuatro import Cuatro
from Servers.Descargar import Descargar

from Servers.utiles import salir, windows_end, PdtVersion

class Servidor(object):
    '''
        Contiene los métodos para identificar a que servidor (tv) pertenece la url que
        introdujo el usuario.
    '''
    def __init__(self, url=None):
        '''
            Lo único a resalar es que reibirá la URL
        '''
        self._url = url
    def isAntena3_(self):
        '''
            return True si la URL pertenece a antena 3
        '''
        if self._url.find("antena3.com") != -1:
            return True
    def isTVE_(self):
        '''
            return True si la URL pertenece a Televisión Española
        '''
        if self._url.find("rtve.es") != -1:
            return True
    #def isTVEaLaCarta_(self): # DEPRECATED
    #    if self._url.find("rtve.es") != -1 and self._url.find("/alacarta/") != -1:
    #        return True
    def isRTVE_(self):
        '''
            return True si la URL pertenece a los audios de a web de telvión española (Radio Nacional)
        '''
        if self._url.find("rtve.es") != -1 and \
            (self._url.find("/mediateca/audios/") != -1 or self._url.find("/alacarta/audios/") != -1):
            return True
    def isT5_(self):
        '''
            return True si la URL pertenece a Telecinco
        '''
        if self._url.find("telecinco.es") != -1:
            return True
    def isLaSexta_(self):
        '''
            return True si la URL pertenece a La Sexta
        '''
        if self._url.find("lasexta.com/sextatv/") != -1:
            return True
    def isCuatro_(self):
        '''
            return True si la URL pertenece a Cuatro
        '''
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
        y devuelve el objeto según el servicio que del cual se haya pasado la
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
        print "[INFO] Audio de RTVE.es"
        return RTVE(url)
    elif server.isTVE:
        print "[INFO] Vídeo de RTVE.es"
        return TVE(url)
    elif server.isT5:
        print "[INFO] Telecinco"
        return Telecinco(url)
    elif server.isLaSexta:
        salir("La Sexta: Todavía no implementado")
        # return LaSexta(url)
    elif server.isCuatro:
        salir("Cuatro: Todavía no implementado")
        # return Cuatro(url)
    else:
        msgErr = "ERROR: La URL \"" + url + "\" no pertenece a ninguna Televisión"
        salir(msgErr)
        
def comprobar_version():
    '''
        Comprueba la versión del cliente con la última lanzada utilizando la clase
        PdtVersion() de utilies.py
    '''
    pdtv = PdtVersion()
    try:
        pdtv.comp_version(pdtv.get_new_version())
    except:
        print "[!!!] ERROR al comprobar la versión del cliente"
        
def help(args):
    '''
        Muestra la ayuda por pantalla (se le pasa como argumento siempre: argv)
    '''
    print "USO:", args[0]
    print "o   ", args[0], "<url>"
    print "(Los dos métodos aceptan varias URLs separadas por un espacio)"
    print "PyDownTV <aabilio@gmail.com>"

def windowsPresentation():
    '''
        Muestra un presetación cuando se ejecuta en Windows
    '''
    print "PyDownTV",  __version__
    print "======================="
    print u"Descarga los vídeos de las webs de las TVs".encode("cp850")

def compURL(url):
    '''
        Comara de foma muy básica si la cadena que se le pasa como parámetro es una URL válida
    '''
    #p = re.compile('^http://.+\..+$', re.IGNORECASE)
    p = re.compile('^(https?)://([-a-z0-9\.]+)(?:(/[^?\s]+)?)?$', re.IGNORECASE)
    m = p.match(url)
    if m:
        return True
    else:
        return False



if __name__ == "__main__":
    if platform == "win32" and len(argv) == 1:
        windowsPresentation()
    
    # Comprobar la versión del cliente
    comprobar_version()
    
    # Ver si tenemos un parámetro, si no tenemos parámetro pedir la URL por 
    # entrada estándar.
    url = None
    if len(argv) >= 2:
        #exit("ERROR: Demasiados parámetros.\nFlag --help: para ayuda")
        if argv[1] == "--help" or argv[1] == "-h":
            help(argv)
            salir("")
        i = ""
        url = []
        for i in argv[1:]:
            url.append(i)
        nOfUrls = len(url)
    else:
        try:
            inPut = raw_input("Introduce las URL de los vídeos (separadas por espacios):\n")
            url = inPut.split(" ")
            
            todasvacias = True
            for i in url:
                if i != "":
                    todasvacias = False
            if todasvacias:
                url = None
            
            if url is not None:
                nOfUrls = len(url)
        except KeyboardInterrupt:
            salir("\nBye!")

    if url != None:
        # Comprobar la url y mandarla al servidor correspondiente
        cuantasIncorrectas = 0
        cuantasTotal = nOfUrls
        while nOfUrls-1 >= 0:
            if compURL(url[nOfUrls-1]):
                # URL comprobada: http://"algo.algo"
                servidor = qServidor(url[nOfUrls-1]) # Devuelve el objeto de la clase correspondiente
            else:
                cuantasIncorrectas += 1
                print "[!] URL incorrecta:",  url[nOfUrls-1]
                #exit("ERROR: URL mal introducida\nFlag --help: para ayuda")
            nOfUrls -= 1
        if cuantasIncorrectas == cuantasTotal:
            salir("[!!!] Todas las URLs son incorrectas")
    else:
        salir("No has introducido la URL!")

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
    windows_end()
