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
__version__ = "3.3-BETA"

from sys import argv, exit, platform
import re

#from ui.gui import Ui_MainWindow

# Ir añadiendo según se implementen
from Servers.a3 import A3
from Servers.tve import TVE
from Servers.rtve import RTVE
# DEPRECATED from Servers.tvalacarta import TvAlacarta
from Servers.telecinco import Telecinco
from Servers.lasexta import LaSexta
from Servers.cuatro import Cuatro
from Servers.crtvg import CRTVG
from Servers.btv import BTV
from Servers.canalsur import CSur
from Servers.rtvv import RTVV
from Servers.tv3 import TV3
from Servers.eitb import EITB
from Servers.extremadura import ETV
from Servers.televigo import TeleVigo
from Servers.tvamurcia import TVAmurcia
from Servers.intereconomia import Intereconomia
from Servers.giraldatv import GiraldaTV
from Servers.riasbaixas import RiasBaixas
from Servers.rtvcyl import RTVCYL
from Servers.rtvc import RTVC
from Servers.rtvcm import RTVCM
from Servers.planetaurbe import PlanetaUrbe
from Servers.Descargar import Descargar

from Servers.utiles import salir, windows_end, PdtVersion, printt

class Servidor(object):
    '''
        Contiene los métodos para identificar a que servidor (tv) pertenece la url que
        introdujo el usuario.
    '''
    def __init__(self, url=None):
        '''Lo único a resaltar es que reibirá la URL'''
        self._url = url
    def isAntena3_(self):
        '''return True si la URL pertenece a antena 3'''
        if self._url.find("antena3.com") != -1:
            return True
    def isTVE_(self):
        '''return True si la URL pertenece a Televisión Española'''
        if self._url.find("rtve.es") != -1:
            return True
    #def isTVEaLaCarta_(self): # DEPRECATED
    #    if self._url.find("rtve.es") != -1 and self._url.find("/alacarta/") != -1:
    #        return True
    def isRTVE_(self):
        '''return True si la URL pertenece a los audios de a web de telvión española (Radio Nacional)'''
        if self._url.find("rtve.es") != -1 and \
            (self._url.find("/mediateca/audios/") != -1 or self._url.find("/alacarta/audios/") != -1):
            return True
    def isT5_(self):
        '''return True si la URL pertenece a Telecinco'''
        if self._url.find("telecinco.es") != -1:
            return True
    def isLaSexta_(self):
        '''return True si la URL pertenece a La Sexta'''
        if self._url.find("lasexta.com/") != -1 or self._url.find("lasextadeportes.com") != -1:
            return True
    def isCuatro_(self):
        '''return True si la URL pertenece a Cuatro'''
        if self._url.find("cuatro.com/") != -1:
            return True
    def isCRTVG_(self):
        '''return True is la URL pertenece a TV de Galiza'''
        if self._url.find("crtvg.es/") != -1:
            return True
    def isBTV_(self):
        '''return True si la URL pertenece a BTV'''
        if self._url.find("btvnoticies.cat") != -1 or self._url.find("btv.cat/alacarta") != -1:
            return True
    def isCSur_(self):
        '''return True si la URL pertenece a Canal Sur TV'''
        if self._url.find("canalsuralacarta.es") != -1 or self._url.find("canalsur.es") != -1:
            return True
    def isRTVV_(self):
        '''return True si la URL pertenece a Ràdio Televisió Valenciana'''
        if self._url.find("rtvv.es") != -1:
            return True
    def isTV3_(self):
        '''return True si la url perteneces a TV3'''
        if self._url.find("tv3.cat") != -1 or self._url.find("3cat24.cat") != -1 or self._url.find("catradio.cat") != -1:
            return True
    def isEITB_(self):
        '''return True si la url pertenece a EITB'''
        if self._url.find("eitb.com") != -1:
            return True
    def isETV_(self):
        '''return True si la url pertenece a extremadura TV'''
        if self._url.find("canalextremadura.es/") != -1:
            return True
    def isTeleVigo_(self):
        '''return True si la url pertenece a TeleVigo'''
        if self._url.find("televigo.com/") != -1:
            return True
    def isTVAmurcia_(self):
        '''return True si la url pertenece a la televisión autonómica de Murcia'''
        if self._url.find("7rm.es/") != -1:
            return True
    def isIntereconomia_(self):
        '''return True si la url pertenecea Intereconomia'''
        if self._url.find("intereconomia.com/") != -1:
            return True
    def isGiraldaTV_(self):
        '''return True si la url pertenece a Giralda TV'''
        if self._url.find("giraldatv.es/") != -1:
            return True
    def isCanalRiasBaixas_(self):
        '''return True si la url pertenece a Canal Rías Baixas'''
        if self._url.find("canalriasbaixas.com/") != -1:
            return True
    def isRTVCYL_(self):
        '''return True si la utl pertenecea Radio TV de Castilla y León'''
        if self._url.find("rtvcyl.es/") != -1:
            return True
    def isRTVC_(self):
        '''return True si la url pertenece a RTVC'''
        if self._url.find("rtvc.es/") != -1:
            return True
    def isRTVCM_(self):
        '''return True si la url pertenece a RTV de Castilla - La Mancha'''
        if self._url.find("rtvcm.es/") != -1:
            return True
    def isPlanetaUrbe_(self):
        '''return True si la url pertenece a PlanetaUrbe.tv'''
        if self._url.find("planetaurbe.tv/") != -1:
            return True
    
    # COMPLEMENTAR CON LOS DIFERENTES SERVIDORES QUE SE VAYAN SOPORTANDO
    
    isAntena3 = property(isAntena3_)
    isTVE = property(isTVE_)
    # DEPRECATED isTVEaLaCarta = property(isTVEaLaCarta_)
    isRTVE = property(isRTVE_)
    isT5 = property(isT5_)
    isLaSexta = property(isLaSexta_)
    isCuatro = property(isCuatro_)
    isCRTVG = property(isCRTVG_)
    isBTV = property(isBTV_)
    isCSur = property(isCSur_)
    isRTVV = property(isRTVV_)
    isTV3 = property(isTV3_)
    isEITB = property(isEITB_)
    isETV = property(isETV_)
    isTeleVigo = property(isTeleVigo_)
    isTVAmurcia = property(isTVAmurcia_)
    isIntereconomia = property(isIntereconomia_)
    isGiraldaTV = property(isGiraldaTV_)
    isCanalRiasBaixas = property(isCanalRiasBaixas_)
    isRTVCYL = property(isRTVCYL_)
    isRTVC = property(isRTVC_)
    isRTVCM = property(isRTVCM_)
    isPlanetaUrbe = property(isPlanetaUrbe_)
    
def qServidor(url):
    '''
        Comprueba utlizando la clase Servidor de que servicio ha recibido la url
        y devuelve el objeto según el servicio que del cual se haya pasado la
        url
    '''
    # Descomentar return según se vañan añadiendo
    server = Servidor(url)
    if server.isAntena3:
        printt(u"[INFO] Antena 3 Televisión")
        return A3(url)
    #elif server.isTVEaLaCarta: # DEPRECATED
    #    print "[INFO] TV Española \"A la carta\""
    #    return TvAlacarta(url)
    elif server.isRTVE: # Tienes que comprobarse antes que isTVE
        printt(u"[INFO] Audio de RTVE.es")
        return RTVE(url)
    elif server.isTVE:
        printt(u"[INFO] Vídeo de RTVE.es")
        return TVE(url)
    elif server.isT5:
        printt(u"[INFO] Telecinco")
        return Telecinco(url)
    elif server.isLaSexta:
        printt(u"[INFO] La Sexta")
        return LaSexta(url)
    elif server.isCuatro:
        printt(u"[INFO] Cuatro")
        printt(u"[!!!] Actualmente los vídeos de Play Cuatro dan ERROR")
        return Cuatro(url)
    elif server.isCRTVG:
        printt(u"[INFO] Televisión de Galiza")
        return CRTVG(url)
    elif server.isBTV:
        printt(u"[INFO] Barcelona Televisió")
        return BTV(url)
    elif server.isCSur:
        printt(u"[INFO] Canal Sur")
        return CSur(url)
    elif server.isRTVV:
        printt(u"[INFO] Ràdio Televisió Valenciana")
        return RTVV(url)
    elif server.isTV3:
        printt(u"[INFO] TV3")
        return TV3(url)
    elif server.isEITB:
        printt(u"[INFO] EITB")
        return EITB(url)
    elif server.isETV:
        printt(u"[INFO] Radio Televisión de Extremadura")
        return ETV(url)
    elif server.isTeleVigo:
        printt(u"[INFO] Tele Vigo")
        return TeleVigo(url)
    elif server.isTVAmurcia:
        printt(u"[INFO] TV Autonómica de Murcia")
        return TVAmurcia(url)
    elif server.isIntereconomia:
        printt(u"[INFO] Intereconomía")
        return Intereconomia(url)
    elif server.isGiraldaTV:
        printt(u"[INFO] Giralda Televisión")
        return GiraldaTV(url)
    elif server.isCanalRiasBaixas:
        printt(u"[INFO] canalriasbaixas.com")
        return RiasBaixas(url)
    elif server.isRTVCYL:
        printt(u"[INFO] Radio Televisión de Castilla y León")
        return RTVCYL(url)
    elif server.isRTVC:
        printt(u"[INFO] Radio Televisión Canaria")
        return RTVC(url)
    elif server.isRTVCM:
        printt(u"[INFO] Radio Televisión de Castilla - La Mancha")
        return RTVCM(url)
    elif server.isPlanetaUrbe:
        printt(u"[INFO] Planeta Urbe TV")
        return PlanetaUrbe(url)
    else:
        msgErr = u"ERROR: La URL \"" + url + u"\" no pertenece a ninguna Televisión soportada"
        salir(msgErr)
        
def comprobar_version():
    '''
        Comprueba la versión del cliente con la última lanzada utilizando la clase
        PdtVersion() de utilies.py
    '''
    printt(u"[INFO VERSIÓN] Comprobando si existen nuevas versiones de PyDownTV")
    pdtv = PdtVersion()
    try:
        new_version, changelog = pdtv.get_new_version()
        if new_version == -1:
            printt(u"[!!!] ERROR al comprobar la versión del cliente")
        else:
            pdtv.comp_version(new_version, changelog)
    except KeyboardInterrupt:
        printt(u"[+] Comprobación cancelada")
    except Exception:
        printt(u"[!!!] ERROR al comprobar la versión del cliente")
        
def help(args):
    '''
        Muestra la ayuda por pantalla (se le pasa como argumento siempre: argv)
    '''
    printt(u"USO:", args[0])
    printt(u"o   ", args[0], u"[opciones] <url>")
    printt(u"Opciones:")
    printt(u"  - \"--help\": Muestra esta ayuda")
    printt(u"  - \"--no-check-version\": No comprueba si existen nuevas versiones de PyDownTV")
    printt(u"(Los dos métodos aceptan varias URLs separadas por un espacio)")
    printt(u"PyDownTV <aabilio@gmail.com>")

def windowsPresentation():
    '''
        Muestra un presetación cuando se ejecuta en Windows
    '''
    printt(u"||=============================")
    printt(u"|| PyDownTV", __version__, u"[Windows]")
    printt(u"||=============================")
    printt(u"|| Descarga los vídeos de las webs de las TVs")
    printt(u"||___________________________________________")
    print ""
    
def nixPresentation():
    '''
        Muestra presentación cuando se ejecuta en sistemas *nix
    '''
    printt(u"||===================")
    printt(u"|| PyDownTV", __version__)
    printt(u"||===================")
    printt(u"|| Descarga los vídeos de las webs de las TVs")
    printt(u"||___________________________________________")
    print ""
    
def compURL(url):
    '''
        Compara de forma muy básica si la cadena que se le pasa como parámetro es una URL válida
    '''
    # El primero que tuve (básico):
    #p = re.compile('^http://.+\..+$', re.IGNORECASE)
    # La siguiente no valida los vídeos de la TVG:
    #p = re.compile('^(https?)://([-a-z0-9\.]+)(?:(/[^?\s]+)(?:\?((?:\w+=\w+)?(?:&\w+=\w+)*)?)?)?$', re.IGNORECASE)
    p = re.compile('^(https?)://([-a-z0-9\.]+)(?:(/[^?\s]+)(?:\?((?:\w+=[-a-z0-9/%:,._]+)?(?:&\w+=[-a-zA-Z0-9/%:,._]+)*)?)?)?$', re.IGNORECASE)
    m = p.match(url)
    if m:
        return True
    else:
        return False



if __name__ == "__main__":
    if platform == "win32" and len(argv) == 1:
        windowsPresentation()
    elif platform != "win32" and len(argv) == 1:
        nixPresentation()
    
    
    # Ver si tenemos un parámetro, si no tenemos parámetro pedir la URL por 
    # entrada estándar.
    url = None
    if len(argv) >= 2:
        #exit("ERROR: Demasiados parámetros.\nFlag --help: para ayuda")
        if argv[1] == "--help" or argv[1] == "-h":
            help(argv)
            salir(u"")
            
            
        i = ""
        url = []
        
        if argv[1] == "--no-check-version":
            for i in argv[2:]:
                url.append(i)
        elif argv[1] == "--show" or argv[1] == "-s":
            for i in argv[2:]:
                url.append(i)
        else:
            comprobar_version()
            for i in argv[1:]:
                url.append(i)
                
        nOfUrls = len(url)
    else:
        try:
            comprobar_version()
            
            printt(u"\n[--->] Introduce las URL de los vídeos (separadas por espacios):")
            inPut = raw_input()
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
            salir(u"\nBye!")

    if url != None:
        if len(url) == 0:
            salir(u"No has introducido ninguna URL!")
        # Comprobar la url y mandarla al servidor correspondiente
        cuantasIncorrectas = 0
        cuantasTotal = nOfUrls
        while nOfUrls-1 >= 0:
            if compURL(url[nOfUrls-1]):
                # URL comprobada: http://"algo.algo"
                servidor = qServidor(url[nOfUrls-1]) # Devuelve el objeto de la clase correspondiente
            else:
                cuantasIncorrectas += 1
                printt(u"[!] URL incorrecta:",  url[nOfUrls-1])
                #exit("ERROR: URL mal introducida\nFlag --help: para ayuda")
            nOfUrls -= 1
        if cuantasIncorrectas == cuantasTotal:
            salir(u"[!!!] Todas las URLs son incorrectas (empiezan por: http://)")
    else:
        salir(u"No has introducido ninguna URL!")
        
    # SOLO MOSTRAR ENLACES
    for i in argv:
        if i == "--show" or i == "-s":
            printt(u"[INFO] Solo mostrar enlaces:")
            urlDeDescarga, outputName = servidor.procesarDescarga()
            for i in urlDeDescarga:
                printt(u"%s" % i)
            salir(u"")

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
