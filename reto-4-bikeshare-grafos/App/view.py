"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import threading
import controller
assert cf
from prettytable import PrettyTable, ALL
from DISClib.ADT import list as lt

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

bikesharefile = 'Bikeshare/Bikeshare-ridership-2021-utf8-small.csv'
cont = None

def newController(listType):
    """
    Se crea una instancia del controlador
    """
    control = controller.newController(listType)
    return control

def printMenu():
    print("\nBienvenido querido usuario <3:")
    print("1- Cargar información en el catálogo")
    print("2- Comprar bicicletas para las estaciones con más viajes de origen")
    print("3- Planear paseos turísticos por la ciudad")
    print("4- Reconocer los componentes fuertemente conectados del sistema")
    print("5- Planear una ruta rápida para el usuario")
    print("6- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7- Planear el mantenimiento preventivo de bicicletas")
    print("8- La estación más frecuentada por los visitantes")
    print("0- Salir")

def printSimplePrettyTable(spotifyList, keys):
    table = PrettyTable()
    table.max_width = 20
    table.hrules = ALL
    table.field_names = keys
    rows = []
    for element in lt.iterator(spotifyList):
        row = []
        for key in keys:
            strElement = str(element[key])
            if len(strElement) > 20:
                strElement = strElement[:20]
            row.append(strElement)
        rows.append(row)
    table.add_rows(rows)
    print(table)


def printSimplePrettyTableWOLIMT(spotifyList, keys):
    table = PrettyTable()
    #table.max_width = 20
    table.hrules = ALL
    table.field_names = keys
    rows = []
    for element in lt.iterator(spotifyList):
        row = []
        for key in keys:
            strElement = str(element[key])
            row.append(strElement)
        rows.append(row)
    table.add_rows(rows)
    print(table)

def headers(req_num, messageone, messagetwo):
    print("\n============= Req No. " + str(req_num) + " Inputs =============")
    print(messageone)
    print("\n============= Req No. " + str(req_num) + " Answer =============" )
    print(messagetwo)

def printHeadersTop(reqNum, firstMessage):
    print("\n============= Req No. " + str(reqNum) + " Inputs =============")
    print(firstMessage)

def printHeadersBottom(reqNum, secondMessage):
    print("============= Req No. " + str(reqNum) + " Answer =============" )
    print(secondMessage)

"""
Menu principal
"""
def thread_cycle():
    while True:
        try:
            printMenu()
            inputs = input('Seleccione una opción para continuar: ')
            if int(inputs[0]) == 1:
                print("\nInicializando ....")
                cont = controller.init()
                print("\nCargando la información ....")
                linescounted, deleted, answerListDG, answerListND = controller.loadData(cont, bikesharefile)
                print('Grafos cargados ....')
                message1= str(linescounted)+ ' trips in CSV file...\n' + str(deleted) + ' trips with incomplete data and were cleaned...\n' + '\n'+ str(controller.stationSize(cont)) +' unique stations loaded...\n' + str(controller.edgesSize(cont)) + ' clean avg trips data loaded...\n'
                message2= '\n--- DiGraph specs --- \nNodes: ' + str(controller.stationSize(cont)) + ' & Edges: ' + str(controller.edgesSize(cont)) + '\nFirst 5 & Last 5 Stations loaded in the Digraph.'
                printHeadersTop('Bike-Trips-Time DiGraphs', message1 + message2)
                printSimplePrettyTable(answerListDG, ['Station ID', 'Station Name', 'In Degree (Routes)','Out Degree (Routes)', 'In Trips (TOTAL)', 'Out Trips (TOTAL)'])
                print('\n--- Graph specs --- \nNodes: ' + str(controller.stationSizeND(cont)) + ' & Edges: ' + str(controller.edgesSizeND(cont)) + '\nFirst 5 & Last 5 Stations loaded in the Digraph.')
                printSimplePrettyTable(answerListND, ['Station ID', 'Station Name', 'Degree (Rep Routes)', 'roundTrips'])

            elif int(inputs[0]) == 2:
                top5Stations = controller.topFive5Stations(cont)
                message1 = 'TOP 5 stations inside in the Bikeshare Network. \nNumber of stations in the network: ' + str(controller.stationSize(cont))
                message2 = 'TOP 5 stations used as trips origins are:'
                headers(1, message1, message2)
                printSimplePrettyTable(top5Stations, ['Station ID', 'Station Name','Out Trips (TOTAL)', 'Suscriber Out Trips', 'Tourist Out Trips', 'Out Degree (Routes)', 'Rush hour', 'Rush Date' ])

            elif int(inputs[0]) == 3:
                maxTime = int(input('Ingrese el tiempo máximo disponible para su paseo en segundos: ').strip())
                minJumps = int(input('Ingrese el minimo de estaciones de parada para su ruta (no incluya la estacion de origen): ').strip())
                TOP = int(input('Ingrese el maximo numero de rutas que desea ver: ').strip())
                startStation = input('Ingrese la estacion de la cual quiere iniciar: ').strip()
                howManyRoutes, startStationID, ltRoutesANS = controller.possibleRoutesTimeandSpace(cont, startStation, maxTime, minJumps, TOP)
                message1 = 'Available time: {0} \nAvailable time: {1} \nMinimum number of stations: {2} \nMaximum number of routes: {3} \nStarting station: {4}'.format(maxTime, maxTime, minJumps, TOP, startStation)
                message2 = ('There are {0} possible routes from station: \n      {1}:{2} \n\n+++ The TOP {3} ROUTES ARE: +++ \nThe first 3 and last 3 possible routes are:').format(howManyRoutes, startStationID, startStation, TOP)
                headers(2, message1, message2)
                printSimplePrettyTableWOLIMT(ltRoutesANS, ['Stop Stations', 'Route time [s]','Route time [m]', 'Station IDs', 'Station names' ])

            elif int(inputs[0]) == 4:
                howMany, SCComponents = controller.SCComponents(cont)
                message1 = '+++ calculating the strongly cinnected components +++ '
                message2 = 'There are {0} Strongly Connected Components (SCC) in the graph. \n\n +++ The SCC details are: +++ \n The first 3 and last 3 of the SCC are: '.format(howMany)
                headers(3, message1, message2)
                printSimplePrettyTable(SCComponents, ['SCC Size', 'SCC ID', 'Max out station ID', 'Max out station name', 'Max out station trips', 'Max in station ID', 'Max in station name', 'Max in station trips'])

            elif int(inputs[0]) == 5:
                startStation = input('Ingrese la estacion de origen: ').strip()
                endStation = input('Ingrese la estacion de llegada: ').strip()
                startStationID, endStationID, howManyStations, totaltime, listPathAns = controller.quickRoute(cont, startStation, endStation)
                message1 = 'Start station: {0} with: {1} trips \nEnd station: {2} with: {3} trips'.format(startStation, startStationID, endStation, endStationID)
                message2 = "\n+++ Dijkstra's Trip Detail +++ \nNumber of stops {0} \nTotal time: {1} [sec]. \nTotal time: {2} [min].  ".format(howManyStations, totaltime, round(totaltime/60, 2))
                headers(4, message1, message2)
                printSimplePrettyTable(listPathAns, ['Start Station ID', 'Start Station Name', 'End Station ID', 'End Station Name', 'Avg Route Duration'])

            elif int(inputs[0]) == 6:
                startDate = input('Ingrese la fecha de inicio (dd/mm/yyyy) que desea consultar: ').strip()
                endDate = input('Ingrese la fecha de fin (dd/mm/yyyy) que desea consultar: ').strip()
                totalTrips, totalTimeSEC, totalTimeHOUR, totalUniqueStation, ltOUTTrips, ltINTrips, keyMaxOutHour,MaxOuHour, keyMaxInHour, MaxInHour = controller.routesDateRange(cont, startDate, endDate)
                message1 = 'Analyze trips between {0} and {1}'.format(startDate, endDate)
                message2 = '{0} trips between {1} and {2}. \n\n{3} unique stations loaded... \n\n{4} clean avg trips loaded... \n\nTotal trip time: {5} [sec]. \n\nTotal trip time: {6} [h].\n\n +++ Top OUT station data: +++ \n'.format(totalTrips, startDate, endDate, totalUniqueStation, totalTrips, totalTimeSEC,totalTimeHOUR)
                headers(5, message1, message2)
                printSimplePrettyTable(ltOUTTrips, ['Station ID', 'Station Name', 'Out Trips  (TOTAL Suscribers)'])
                print('\n+++ Top IN station data: +++')
                printSimplePrettyTable(ltINTrips, ['Station ID', 'Station Name', 'In Trips  (TOTAL Suscribers)'])
                print('\n+++ RUSH HOUR INFO: +++')
                print('\nThe hour in which more trips were starter (in the station) is: ' + str(keyMaxOutHour) + ' with ' + str(MaxOuHour) + ' trips. \nThe hour in which more trips were ended (in the station) is: ' + str(keyMaxInHour) + ' with ' + str(MaxInHour) + ' trips.')

            elif int(inputs[0]) == 7:
                bikeID = int(input('Ingrese el ID de la bicicleta que desea consultar: ').strip())
                totalTripsDone, totalTripsTimeSeconds, totalTripTimeHours, uniqueStation, ansLtOut, ansLtIn = controller.preventiveBike(cont, bikeID)
                message1 = 'Analyze trips with the bike ID {0}.'.format(str(bikeID))
                message2 = '{0} Trips with bike ID {1}. \n\n {2} unique stations loaded... \n\n{3} clean avg trips data loaded...\n\nTotal trip time: {4} [sec]. \n\nTotal trip time: {5} [h].\n\n +++ Top OUT station data: +++'.format(totalTripsDone, bikeID, uniqueStation, totalTripsDone, totalTripsTimeSeconds, totalTripTimeHours)
                headers(6, message1, message2)
                printSimplePrettyTable(ansLtOut, ['Station ID', 'Station Name', 'Out Trips (TOTAL)'])
                print('\n+++ Top IN station data: +++')
                printSimplePrettyTable(ansLtIn, ['Station ID', 'Station Name', 'In Trips (TOTAL)'])

            elif int(inputs[0]) == 8:
                pass

            else:
                sys.exit(0)
        except:
            input("Ingreso una opcion invalida, intentelo de nuevo. Oprima ENTER para continuar...")
            continue

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()