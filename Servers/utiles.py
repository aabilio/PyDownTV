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
