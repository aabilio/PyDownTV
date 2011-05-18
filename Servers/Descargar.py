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

# Clase que se encarga de descargar:

__author__="aabilio"
__date__ ="$30-mar-2011 20:57:46$"

import urllib2
import urllib
import sys
import codecs
from os import system, path

from pyaxel import pyaxel
from utiles import salir, printt, PdtVersion


class Descargar(object):
    ''' Clase que se encarga de descargar con urllib2 '''
    
    std_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; '
        'en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/xml,application/xml,application/xhtml+xml,'
        'text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    'Accept-Language': 'en-us,en;q=0.5',
    }

    def __init__(self, url=None):
        self._outputName = None
        self._URL = url
        if self._URL == None:
            salir(u"ERROR: No se puede descargar la url")
    
    def getOutputName(self):
        return self._outputName
    def setOutputName(self, name):
        self._outputName = name
    
    outputName = property(getOutputName, setOutputName)

    def descargar(self):
        '''
            Recoge una url la descarga y lo devuelve
            Pensado para descargar streams HTML y XML
        '''

        if self._URL.find("http://") == -1:
            self._URL = "http://" + self._URL

        try:
            # TVG necesita headers:
            if self._URL.find("crtvg.es/") != -1:
                request = urllib2.Request(self._URL, None, self.std_headers)
                f = urllib2.urlopen(request)
                stream = f.read()
                f.close()
                return stream
            elif self._URL == PdtVersion.URL_VERSION: # Si lo que se descarga es VERSION (convertir a utf-8)
                f = urllib2.urlopen(self._URL)
                Reader = codecs.getreader("utf-8")
                fh = Reader(f)
                stream = fh.read()
                return stream
            else:
                f = urllib2.urlopen(self._URL)
                stream = f.read()
                f.close()
                return stream
        except Exception, e:
            if self._URL.find("rtve.es") != -1: # No salir (para identificar si es a la carta o no)
                return -1
            elif self._URL == PdtVersion.URL_VERSION:
                return -1
            else:
                print e
                salir(u"[!!!] ERROR al descargar:")
        else:
            pass
            
    def descargarVideoWindows(self, nombre=None):
        url = self._URL
        name = nombre if nombre != None else self._URL.split('/')[-1]
        
        printt(u"")
        printt(u"DESCARGAR:")
        printt(u"----------------------------------------------------------------")

        if type(self._URL) == list:
            b=1
            for i in self._URL:
                printt(u"[ URL DE DESCARGA FINAL ] [Parte %d] %s" % (b, i))
                b += 1
        else:
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)
            
        printt(u"[INFO] Presiona \"Ctrl + C\" para cancelar")
        printt(u"")
        
        def estadodescarga(bloque, tamano_bloque, tamano_total):
            '''
                función reporthook que representa en pantalla información mientras
                se realiza la descarga
            '''
            # En Megas
            try:
                cant_descargada = ((bloque * tamano_bloque) / 1024.00) / 1024.00
                tamano_total = (tamano_total / 1024.00) / 1024.00
                porcentaje = cant_descargada / (tamano_total / 100.00)
                if porcentaje > 100.00:
                    porcentaje = 100.00
            except ZeroDivisionError:
                pass
                #print "[DEBUG] Error de divisiñon entre cero"
            # TODO: Agregar velocidad de descarga al progreso
            sys.stdout.write("\r[Descargando]: [ %.2f MiB / %.2f MiB ]\t\t[ %.1f%% ]" \
                            % (cant_descargada, tamano_total, porcentaje))
        
        if type(self._URL) == list:
            for i in range(0, len(self._URL)):
                printt(u"[Descargando %d parte]" % (int(i) + 1))
                printt(u"[Destino]", name[i])
                try:
                    urllib.urlretrieve(url[i], name[i], reporthook=estadodescarga)
                    print ""
                except KeyboardInterrupt:
                    sys.exit("\nCiao!")
                    
                if i < len(self._URL)-1: 
                    printt(u"==================================")
                    printt(u"")
                    printt(u"Parte descargada o cancelanda")
                    printt(u"Presiona [ENTER] para continuar")
                    printt(u"Presiona[Ctrl + C] para Cancelar")
                    printt(u"")
                    printt(u"==================================")
                    try:
                        raw_input()
                    except KeyboardInterrupt:
                        salir(u"\nBye!")
        else:
            try:
                printt(u"[Destino]", name)
                urllib.urlretrieve(url, name, reporthook=estadodescarga)
                print ""
            except KeyboardInterrupt:
                salir("\nCiao!")

    def descargarVideo(self):
        '''
            Procesa la descarga del vídeo llamanda a la función download de pyaxel para la mayoría de los
            vídeos en GNU/Linux y Mac OS X. Para sistemas win32, se llama a descargarVideoWindows() y tanto para
            GNU/Linux como para Mac OS X y Windows cuando el protocolo es mms:// se utiliza libmms (por ahora Windows no)
            y cuando el protocolo es rtmp:// se utiliza el binario rtmpdump que el cliente debe tener instalado.
        '''
        # Utilizar el binario de rtmpdu si el protocolo es rtmp://
        if type(self._URL) != list and self._URL.startswith("rtmp://"):
            printt(u"")
            printt(u"DESCARGAR:")
            printt(u"----------------------------------------------------------------")
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)
            printt(u"[   DESTINO   ]", self.outputName)
            printt(u"\n[INFO] Presiona \"Ctrl + C\" para cancelar\n")
            
            rtmpdump = "rtmpdump -o \"" + self.outputName +  "\" -r \"" + self._URL + "\""
            rtmpdump_resume = "rtmpdump --resume -o \"" + self.outputName +  "\" -r \"" + self._URL + "\""
            rtmpdump_win = "rtmpdump.exe -o \"" + self.outputName +  "\" -r \"" + self._URL + "\""
            rtmpdump_resume_win = "rtmpdump.exe --resume -o \"" + self.outputName +  "\" -r \"" + self._URL + "\""

            try:
                if path.isfile(self.outputName):
                    printt(u"Se ha encontrado una descarga parcial anterior, se continúa...\n")
                    printt(u"\nLanzando rtmpdump...\n")
                    if sys.platform == "win32":
                        system(rtmpdump_resume_win)
                    else:
                        system(rtmpdump_resume)
                else:
                    printt(u"\nLanzando rtmpdump...\n")
                    if sys.platform == "win32":
                        system(rtmpdump_win)
                    else:
                        system(rtmpdump)
            except OSError, e:
                printt(u"[!!!] ERROR. No se encuenta rtmpdump:", e)
            except KeyboardInterrupt:
                salir(u"Bye!")
                
            return
            
        #### FIN RTMP://
            
            
        # Utilizar pylibmms si el protocoo es mms://
        if type(self._URL) != list and self._URL.startswith("mms://"):
            # Por ahora solo tengo libmms compilado para Mac OS X
            printt(u"")
            printt(u"DESCARGAR:")
            printt(u"----------------------------------------------------------------")
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)
            printt(u"[   DESTINO   ]", self.outputName)
            
            
            if sys.platform == "win32":
                msg = '''Protocolo MMS aun no disponible en Windows.
                La URL FINAL DE DESCARGA que se muestra, es la localización final del archivo.
                Puedes descargar el archivo mediante esta URL a través de algun gestor de
                descargas que soporte la descarga a través del protocolo mms://
                '''
                printt(msg)
                return
            
            try:
                from pylibmms import core as libmmscore
            except ImportError, e:
                print e
                salir(u"[!!!] ERROR al impotar libmms")
            
            printt(u"\n[INFO] Presiona \"Ctrl + C\" para cancelar\n")
            options = [self._URL, self.outputName]
            libmmscore.run(options)
            
            return
            
        #### FIN MMS://
            
        # Solo en descara normal (para no utilizar pyaxel) por eso los protocolos rtmp:// y mms://
        # NO están incluídos aquí y están antes
        if sys.platform == "win32":
            self.descargarVideoWindows(self.outputName)
            return
            
        #### FIN WINDOWS
        
        #### START PYAXEL
        
        printt(u"")
        printt(u"DESCARGAR:")
        printt(u"----------------------------------------------------------------")
        if type(self._URL) == list:
            b=1
            for i in self._URL:
                printt(u"[ URL DE DESCARGA FINAL ] [Parte %d] %s" % (b, i))
                b += 1
        else:
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)

        
        printt(u"[INFO] Presiona \"Ctrl + C\" para cancelar")
        printt(u"")
        if type(self._URL) == list:
            for i in range(0, len(self._URL)):
                printt(u"[Descargando %d parte]" % (int(i) + 1))
                options = {"output_file": self._outputName[i], "verbose": True, "max_speed": None, "num_connections": 4}
                pyaxel.download(self._URL[i], options)
                if i < len(self._URL)-1: 
                    printt(u"==================================")
                    printt(u"")
                    printt(u"Parte descargada o cancelanda")
                    printt(u"Presiona [ENTER] para continuar")
                    printt(u"Presiona[Ctrl + C] para Cancelar")
                    printt(u"")
                    printt(u"==================================")
                    try:
                        raw_input()
                    except KeyboardInterrupt:
                        salir(u"\nBye!")
            #for (i, b) in (self._URL, self._outputName):
            #    options = {"output_file": b, "verbose": True, "max_speed": None, "num_connections": 4}
            #    pyaxel.download(i, options)
        else:
            options = {"output_file": self._outputName, "verbose": True, "max_speed": None, "num_connections": 4}
            pyaxel.download(self._URL, options)

        
