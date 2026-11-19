"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    analizer = model.newAnalyzer()
    return analizer

# Funciones para la carga de datos

def loadData(analyzer, fifafile):
    """
    Carga los albumes del archivo.
    """
    fifafile = cf.data_dir + fifafile
    input_file = csv.DictReader(open(fifafile, encoding ='utf-8'))
    for player in input_file:
        model.addPlayer(analyzer, player)

# Funciones de ordenamiento

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByClubName(analyzer, clubName):
    answerLstreq = model.playersByClubName(analyzer, clubName)
    return getFirstNum(5, answerLstreq), model.lt.size(answerLstreq)

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByTraits(analyzer, trait, dobMin, dobMax):
    answerLstreq = model.playersByTraitsLst(analyzer, trait, dobMin, dobMax)
    return answerLst(answerLstreq), model.lt.size(answerLstreq)

# Funciones de consulta sobre el catálogo

def playersSize(analyzer):
    """
    Players loaded
    """
    return model.playersSize(analyzer)

def getLastNum(number, fifaList):
    'Retorna los "number" ultimos'
    return model.getLastNum(number, fifaList)

def getFirstNum(number, fifaList):
    'Retorna los "number" primeros'
    return model.getFirstNum(number, fifaList)


# Funciones auxiliares

def answerLst(fifaList, num = 3):
    if model.lt.size(fifaList) <= num * 2:
        return fifaList
    else:
        firsts = getFirstNum(num, fifaList)
        lasts = getLastNum(num, fifaList)
        return model.listsFusion(firsts, lasts)
