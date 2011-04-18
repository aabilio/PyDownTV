#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit, platform

def salir(msg):
    if platform == "win32":
        print msg
        print ""
        end = raw_input("[FIN] Presiona ENTER para SALIR")
        exit()
    else:
        exit(msg)

def formatearNombre(self, nombre):
    '''
        Se le pasa una cadena por parámetro y formatea esta quitándole caracteres
        que pueden colisionar a la hora de realizar el guardado en disco la descarga
        Por ejemplo:
                - Quita las barras "/"
                - Quita los espacios
                - Reduce las barras bajas
                - Elimina las comillas simples
    '''

    nombre = nombre.replace(": ",  ":")
    nombre = nombre.replace('/',"-") # Quitar las barras "/"
    nombre = nombre.replace(" ", "_") # Quirar espacios
    nombre = nombre.replace("_-_", "-")
    nombre = nombre.replace("&#146;", "=") # Cambiar el caracter escapado (') por (=)

    return nombre
