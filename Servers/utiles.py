#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit, platform
import Descargar

class PdtVersion(object):
    
    # Recordar subir antes los archivos a Downloads aumentar la versión en VERSION
    PDT_VERSION = "1.1-BETA"
    URL_VERSION = "http://pydowntv.googlecode.com/svn/trunk/trunk/VERSION"
    CHANGELOG = (
    """
    - Soporte para controlar la versión del cliente
    - Pequeños Bugs arreglados
    """
    )
    
    def __init__(self):
        pass

    def get_new_version(self):
        new_version = Descargar.Descargar(self.URL_VERSION)
        stream_version = new_version.descargar().split("\"")[1]
        #print stream_version
        return stream_version
        
    def comp_version(self, version):
        if self.PDT_VERSION < version:
            print "[INFO] Existe un nueva versión de PyDownTV:", version
            print "[INFO] Cambios en la nueva versión:"
            print self.CHANGELOG
        else:
            pass
            
    def changelog(self):
        return self.CHANGELOG

def salir(msg):
    if platform == "win32":
        print msg
        print ""
        end = raw_input("[FIN] Presiona ENTER para SALIR")
        exit()
    else:
        exit(msg)
    
def windows_end():
    if sys.platform == "win32":
        end = raw_input("[FIN] Presiona ENTER para SALIR")
        sys.exit()

def formatearNombre(nombre):
    '''
        Se le pasa una cadena por parámetro y formatea esta quitándole caracteres
        que pueden colisionar a la hora de realizar el guardado en disco la descarga
        Por ejemplo:
                - Quita las barras "/"
                - Quita los espacios
                - Reduce las barras bajas
                - Elimina las comillas simples
                - Elimina tildes
                - Elimina comillas
    '''

    nombre = nombre.replace(": ",  ":")
    nombre = nombre.replace('/',"-") # Quitar las barras "/"
    nombre = nombre.replace(" ", "_") # Quirar espacios
    nombre = nombre.replace("_-_", "-")
    nombre = nombre.replace("&#146;", "=") # Cambiar el caracter escapado (') por (=)
    nombre = nombre.replace("á", "a")
    nombre = nombre.replace("é", "e")
    nombre = nombre.replace("í", "i")
    nombre = nombre.replace("ó", "o")
    nombre = nombre.replace("ú", "u")

    return nombre
