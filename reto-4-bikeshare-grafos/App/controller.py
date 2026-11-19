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
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de Bicicletas

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer, bikesharefile):
    """
    Carga los albumes del archivo.
    """
    bikesharefile = cf.data_dir + bikesharefile
    input_file = csv.DictReader(open(bikesharefile, encoding = 'utf-8'))
    countlines = 0
    deleted = 0
    for journey in input_file:
        T_Fdeleted = model.addjourney(analyzer, journey)
        if T_Fdeleted:
            deleted += 1
        countlines += 1
    model.createGraphs(analyzer)
    answerListDG, answerListND = model.answerListLoading(analyzer)
    return countlines, deleted, answerListDG, answerListND

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def topFive5Stations(analyzer):
    return model.topFive5Stations(analyzer)

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
def possibleRoutesTimeandSpace(analyzer, startStation, maxTime, minJumps, TOP):
    howManyRoutes, startStationID, ltRoutesANS = model.possibleRoutesTimeandSpace(analyzer, startStation, maxTime, minJumps, TOP)
    return howManyRoutes, startStationID, ltRoutesANS

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
def SCComponents(analyzer):
    howmany, ansLt = model.SCComponents(analyzer)
    return howmany, answerLst(ansLt)

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def quickRoute(analyzer, startStation, endStation):
    startStationID, endStationID, howManyStations, totaltime, listPathAns = model.quickRoute(analyzer, startStation, endStation)
    return startStationID, endStationID, howManyStations, totaltime, listPathAns

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=
def routesDateRange(analyzer, startDate, endDate):
    totalTrips, totalTimeSEC, totalTimeHOUR, totalUniqueStation, ltOUTTrips, ltINTrips, keyMaxOutHour,MaxOuHour, keyMaxInHour, MaxInHour = model.routesDateRange(analyzer, startDate, endDate)
    return totalTrips, totalTimeSEC, totalTimeHOUR, totalUniqueStation, ltOUTTrips, ltINTrips, keyMaxOutHour,MaxOuHour, keyMaxInHour, MaxInHour

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 6]  =^..^=    =^..^=    =^..^=    =^..^=
def preventiveBike(analyzer, bikeID):
    totalTripsDone, totalTripTimeSeconds, totalTripTimeHours, uniqueStation, ansLtOut, ansLtIn = model.preventiveBike(analyzer, bikeID)
    return totalTripsDone, totalTripTimeSeconds, totalTripTimeHours, uniqueStation, ansLtOut, ansLtIn

# Funciones de consulta sobre el catálogo
def stationSize(analyzer):
    """
    Número de estaciones
    """
    return model.stationSize(analyzer)

def edgesSize(analyzer):
    """
    Número de arcos
    """
    return model.edgesSize(analyzer)

def stationSizeND(analyzer):
    """
    Número de estaciones
    """

    return model.stationSizeND(analyzer)

def edgesSizeND(analyzer):
    """
    Número de arcos
    """
    return model.edgesSizeND(analyzer)

def getLastNum(number, fifaList):
    'Retorna los "number" ultimos'
    return model.getLastNum(number, fifaList)

def getFirstNum(number, fifaList):
    'Retorna los "number" primeros'
    return model.getFirstNum(number, fifaList)

def answerLst(fifaList, num = 3):
    if model.lt.size(fifaList) <= num * 2:
        return fifaList
    else:
        firsts = getFirstNum(num, fifaList)
        lasts = getLastNum(num, fifaList)
        return model.listsFusion(firsts, lasts)