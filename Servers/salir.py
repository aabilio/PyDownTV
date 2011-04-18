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
