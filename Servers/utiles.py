#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from sys import exit, platform
import Descargar

def salir(*msg):
    '''
        Recibe una cadena y sustituye al exit() de python para:
        - primero: Parar la ejecución del programa en entornos win32
        - segundo: Mostrar una buena configuración de la codificación en Windows
    '''
    if platform == "win32":
        for i in msg:
            print i.encode("cp850"), 
        print ""
        end = raw_input("[FIN] Presiona ENTER para SALIR")
        exit()
    else:
        for i in msg:
            print i, 
        print ""
        exit()
        
def printt(*msg):
    '''
        Recibe una cadena y la muestra por pantalla en el formato adecuado para sistemas
        win32 y *nix
        Funciona de manera análoga a print de python:
        - con sus concatenaciones de cadenas con '+' o ','
        - con la posibilidad de usar variables directamente o con el formato do especificadore 
          de formato --> printt(u"hola %s eres es usuario número %d" % (user, 925)) p.ejem..
        
        Las cadenas explícitas siempre tienen que tener la 'u' antes de las comillas:
        printt(u"Esto es un mensaje")
        
        printt() ya impreme un caracter de salto de línea final como print
    '''
    if platform == "win32":
        for i in msg:
            print i.encode("cp850"), 
        print ""
    else:
        for i in msg:
            print i, 
        print ""

class PdtVersion(object):
    '''
        Clase que maneja el control de la versión del cliente con las correspondientes
        versiones oficialmente puestas para descargar en la web de proyecto
    '''
    
    # Recordar subir antes los archivos a Downloads aumentar la versión en VERSION
    PDT_VERSION = "2.1-BETA"
    URL_VERSION = "http://pydowntv.googlecode.com/svn/trunk/trunk/VERSION"
    
    def __init__(self):
        pass

    def get_new_version(self):
        '''
            Obtiene y devuelve la última versión oficial lanzada descargándola de URL_VERSION
            y su changelog
        '''
        new_version = Descargar.Descargar(self.URL_VERSION)
        
        # Comprobar que es un formao de versión válido:
        p = re.compile('^\"[0-9]\.[0-9\-].*\".*', re.IGNORECASE)
        m = p.match(new_version.descargar())
        if m:
            stream = new_version.descargar()
            stream_version = stream.split("\"")[1]
            changelog = stream.split("\"")[3]
        
            #print stream_version
            return [stream_version, changelog]
        else:
            return [-1, -1]
        
    def comp_version(self, version, changelog):
        '''
            Compara las versiones y muestra un mensaje con el changelog en caso de que
            exista una versión nueva de el script
        '''
        if self.PDT_VERSION < version:
            printt(u"[INFO] Existe un nueva versión de PyDownTV:", version)
            printt(u"[INFO] Cambios en la nueva versión:")
            printt(changelog)
            # TODO: Añadir URL de descarga aquí y quitar de changelog
        else:
            printt(u"[INFO] Tu versión de PyDownTV es la más reciente")

def windows_end():
    '''
        Para el ciclo del programa a la espera de pulsación de ENTER en
        sistemas win32 al acabar las descargas
    '''
    if platform == "win32":
        end = raw_input("[FIN] Presiona ENTER para SALIR")
        exit()

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
    nombre = nombre.replace("&#146;", "-") # Cambiar el caracter escapado (') por (=)
    nombre = nombre.replace("\'", "-")
    nombre = nombre.replace("\"", "-")
    nombre = nombre.replace("á", "a")
    nombre = nombre.replace("é", "e")
    nombre = nombre.replace("í", "i")
    nombre = nombre.replace("ó", "o")
    nombre = nombre.replace("ú", "u")
    nombre = nombre.replace("ñ", "nh")
    nombre = nombre.replace("\xc3\xb1", "nh") # Cambiar el caracter escapado (ñ) por (nh)

    return nombre
