#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit, platform
from Descargar import Descargar

pdt_version = "1.0"

def get_version():
    D = Descargar("URL para descargar la version")
    return D.descargar()

def comp_version(version):
    if version != pdt_version:
        pass
        # Avisar nuva versión
        # Mostrar Changelog
    else:
        pass
        
def changelog():
    log = """"""

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
