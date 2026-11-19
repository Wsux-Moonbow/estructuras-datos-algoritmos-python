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
import controller
from DISClib.ADT import list as lt
from prettytable import PrettyTable, ALL
assert cf

default_limit = 10000
sys.setrecursionlimit(default_limit * 10000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

fifafile = 'FIFA/fifa-players-2022-utf8-small.csv'
cont = None

def printMenu():
    print("\nBienvenido querido usuario <3:")
    print("1- Cargar información en el catálogo")
    print("2- Reportar las cinco adquisiciones más recientes de un club")
    print("3- Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario")
    print("4- Reportar los jugadores dentro de un rango salarial y con cierta etiqueta")
    print("5- Reportar los jugadores con cierto rasgo característico y nacidos en un periodo de tiempo")
    print("6- Graficar el histograma de una propiedad para los jugadores FIFA")
    print("7- Encontrar posibles sustituciones para los jugadores FIFA")
    print("0- Salir")

def printSimplePrettyTable(fifaList, keys):
    table = PrettyTable()
    table.max_width = 20
    table.hrules = ALL
    table.field_names = keys
    rows = []
    for element in lt.iterator(fifaList):
        row = []
        for key in keys:
            strElement = str(element[key])
            if len(strElement) > 20:
                strElement = strElement[:20]
            row.append(strElement)
        rows.append(row)
    table.add_rows(rows)
    print(table)

def printHeaders(reqNum, firstMessage, secondMessage):
    print("\n============= Req No. " + str(reqNum) + " Inputs =============")
    print(firstMessage)
    print("\n============= Req No. " + str(reqNum) + " Answer =============" )
    print(secondMessage)

def printSearchRange(lower, upper, *args):
    print("\n----- With Search Ranges of -----")
    for tag in args:
        tag = tag[0]
        lower = tag[1]
        upper = tag[2]
        print("\n     * " + str(tag[0]) + " range between " + str(lower) + " and " + str(upper))

def printLeagueDetails(fifaList):
    name = lt.getElement(fifaList,1)['league_name']
    category = int(float(lt.getElement(fifaList,1)['league_level']))
    print("\n----- League Details -----")
    print("     * Name: " + str(name))
    print("     * Category: "  + str(category))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()
        print("\nCargando la información de FIFA players ....")
        controller.loadData(cont, fifafile)
        print('Jugadores cargados: ' + str(controller.playersSize(cont)))
        loadedPlayers = controller.answerLst(cont['players'], 5)
        printSimplePrettyTable(loadedPlayers, ['short_name','age','height_cm','weight_kg','nationality_name'])

    elif int(inputs[0]) == 2:
        clubName = input('Ingrese el nombre del club que desea consultar: ')
        playersByClubName, howMany = controller.playersByClubName(cont, clubName)
        if lt.size(playersByClubName) != 0:
            firstMessage = 'The TOP 5 most recent adquisition of the ' + str(clubName)
            secondMessage = 'There are ' + str(clubName) + ' has ' + str(howMany) + ' adquisitions.'
            printHeaders(3, firstMessage, secondMessage)
            printLeagueDetails(playersByClubName)
            print('\n The last ' + str(howMany) + ' team adquisitions are:')
            printSimplePrettyTable(playersByClubName, ['club_joined','age', 'dob', 'short_name', 'overall', 'nationality_name', 'value_eur', 'wage_eur', 'release_clause_eur', 'club_contract_valid_until', 'player_positions', 'club_position', 'player_tags', 'player_traits'])
        else:
            input('No se encontraron jugadores. Oprima ENTER para continuar...')

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        trait = input('Ingrese el trait que desea consultar: ').strip()
        dobMin = input('Ingrese la fecha minima de nacimiennto: ').strip()
        dobMax = input('Ingrese la fecha maxima de nacimiennto: ').strip()
        playersByTraits, howMany = controller.playersByTraits(cont, trait, dobMin, dobMax)
        printSimplePrettyTable(playersByTraits, ['club_joined','age', 'dob', 'short_name', 'overall', 'nationality_name', 'value_eur', 'wage_eur', 'release_clause_eur', 'club_contract_valid_until', 'player_positions', 'club_position', 'player_tags', 'player_traits'])
        print(howMany)

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
