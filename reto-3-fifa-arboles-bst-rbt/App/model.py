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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mgs
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'players': None}
    analyzer['players'] = lt.newList('ARRAY_LIST')
    analyzer['playersByClubName'] = mp.newMap(numelements = 200, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByTraits'] = mp.newMap(numelements = 1000, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByTraitsLst'] = mp.newMap(numelements = 50, maptype = 'PROBING', loadfactor = 0.5)
    return analyzer

# Funciones para agregar informacion al catalogo

def addPlayer(analyzer, player):
    player['dob'] = stringToDateFormat(player['dob'])
    player['club_joined'] = stringToDateFormat(player['club_joined'])
    player['club_contract_valid_until'] = int(float(player['club_contract_valid_until']))
    player['player_traits'] = player['player_traits'].split(',')
    for characteristic in player:
        if player[characteristic] == '':
            player[characteristic] = 'Unknown'
    lt.addLast(analyzer['players'], player)
    addPlayerByClub(analyzer, player['club_name'], player)
    addPlayerByTrait(analyzer, player)
    addPlayerByTraitLst(analyzer, player)
    if player['sofifa_id'] == '209329':
        print(player['dob'])
        print('bruh')
    return analyzer

def addPlayerByClub(analyzer, clubName, player):
    if mp.contains(analyzer['playersByClubName'], clubName):
        treeByJoin = me.getValue(mp.get(analyzer['playersByClubName'], clubName))
        if om.contains(treeByJoin, player['club_joined']):
            treeByDob = me.getValue(om.get(treeByJoin, player['club_joined']))
            om.put(treeByDob, player['dob'], player)
        else:
            players = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMaxToMin)
            om.put(players, player['dob'], player)
            om.put(treeByJoin, player['club_joined'], players)
    else:
        playersByJoin = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMaxToMin)
        playersByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMaxToMin)
        om.put(playersByDob, player['dob'], player)
        om.put(playersByJoin, player['club_joined'], playersByDob)
        mp.put(analyzer['playersByClubName'], clubName, playersByJoin)

def addPlayerByTrait(analyzer, player):
    for trait in player['player_traits']:
        if mp.contains(analyzer['playersByTraits'], trait):
            treesByDob = me.getValue(mp.get(analyzer['playersByTraits'], trait))
            if om.contains(treesByDob, player['dob']):
                treesByOverall = me.getValue(om.get(treesByDob, player['dob']))
                if om.contains(treesByOverall, player['overall']):
                    treesByPotential = me.getValue(om.get(treesByOverall, player['overall']))
                    if om.contains(treesByPotential, player['potential']):
                        playersByLongname = me.getValue(om.get(treesByPotential, player['potential']))
                        om.put(playersByLongname, player['long_name'], player)
                    else:
                        playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                        om.put(playersByLongname, player['long_name'], player)
                        om.put(treesByPotential, player['potential'], playersByLongname)
                else:
                    treesByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    om.put(playersByLongname, player['long_name'], player)
                    om.put(treesByPotential, player['potential'], playersByLongname)
                    om.put(treesByOverall, player['overall'], treesByPotential)
            else:
                treesByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                treesByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                om.put(playersByLongname, player['long_name'], player)
                om.put(treesByPotential, player['potential'], playersByLongname)
                om.put(treesByOverall, player['overall'], treesByPotential)
                om.put(treesByDob, player['dob'], treesByOverall)
        else:
            treesByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            treesByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            treesByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            om.put(playersByLongname, player['long_name'], player)
            om.put(treesByPotential, player['potential'], playersByLongname)
            om.put(treesByOverall, player['overall'], treesByPotential)
            om.put(treesByDob, player['dob'], treesByOverall)
            mp.put(analyzer['playersByTraits'], trait, treesByDob)

def addPlayerByTraitLst(analyzer, player):
    for trait in player['player_traits']:
        if mp.contains(analyzer['playersByTraitsLst'], trait):
            treesByDob = me.getValue(mp.get(analyzer['playersByTraitsLst'], trait))
            if om.contains(treesByDob, player['dob']):
                lista = me.getValue(om.get(treesByDob, player['dob']))
                lt.addLast(lista, player)
            else:
                lista = lt.newList('ARRAY_LIST')
                lt.addLast(lista, player)
                om.put(treesByDob, player['dob'], lista)
        else:
            treesByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            lista = lt.newList('ARRAY_LIST')
            lt.addLast(lista, player)
            om.put(treesByDob, player['dob'], lista)
            mp.put(analyzer['playersByTraitsLst'], trait, treesByDob)

# Funciones para creacion de datos

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByClubName(analyzer, clubName):
    playersByClubNameArray = lt.newList('ARRAY_LIST')
    entry = mp.get(analyzer['playersByClubName'], clubName)
    if entry:
        playersByClubName = om.valueSet(me.getValue(entry))
        for players in lt.iterator(playersByClubName):
            for player in lt.iterator(om.valueSet(players)):
                lt.addLast(playersByClubNameArray, player)
        return playersByClubNameArray
    return lt.newList()


#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByTraits(analyzer, trait, dobMin, dobMax):
    playersByTraitsArray = lt.newList('ARRAY_LIST')
    entry = mp.get(analyzer['playersByTraits'], trait)
    if entry:
        treesByDob = om.values(me.getValue(entry), stringToDateFormat(dobMin), stringToDateFormat(dobMax))
        for treesByOverall in lt.iterator(treesByDob):
            for treesByPotential in lt.iterator(om.valueSet(treesByOverall)):
                for playersByLongname in lt.iterator(om.valueSet(treesByPotential)):
                    for player in lt.iterator(om.valueSet(playersByLongname)):
                        lt.addLast(playersByTraitsArray, player)
        return playersByTraitsArray
    return lt.newList()

def playersByTraitsLst(analyzer, trait, dobMin, dobMax):
    playersByTraitsArray = lt.newList('ARRAY_LIST')
    entry = mp.get(analyzer['playersByTraitsLst'], trait)
    if entry:
        treesByDob = om.values(me.getValue(entry), stringToDateFormat(dobMin), stringToDateFormat(dobMax))
        for player in lt.iterator(treesByDob):
            for xd in lt.iterator(player):
                lt.addLast(playersByTraitsArray, xd)
        playersByTraitsArray = sortLst(playersByTraitsArray, lt.size(playersByTraitsArray), tmpCmp)
        return playersByTraitsArray
    return lt.newList()

# Funciones de consulta

def playersSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['players'])

def getLastNum(number, fifaList):
    """
    Retorna los primeros number
    """
    if number <= lt.size(fifaList):
        lasts = lt.newList('ARRAY_LIST')
        for cont in range(0, number):
            element = lt.getElement(fifaList, lt.size(fifaList) - cont)
            lt.addFirst(lasts, element)
        return lasts
    else:
        return fifaList

def getFirstNum(number, fifaList):
    """
    Retorna los ultimos number
    """
    if number <= lt.size(fifaList):
        firsts = lt.newList('ARRAY_LIST')
        for cont in range(1, number + 1):
            element = lt.getElement(fifaList, cont)
            lt.addLast(firsts, element)
        return firsts
    else:
        return fifaList

# Funciones utilizadas para comparar elementos

def tmpCmp(e1,e2):
        return e1['dob'] > e2['dob']

def binaryCmp(element1, element2, key):
    'Return True if element1[key] < element2[key], False otherwise.'
    return element1[key] < element2[key]

def cmpKeysMinToMax(k1, k2):
    if (k1 == k2):
        return 0
    elif (k1 > k2):
        return 1
    else:
        return -1

def cmpKeysMaxToMin(k1, k2):
    if (k1 == k2):
        return 0
    elif (k1 < k2):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def sortLst(lst, size, parameter):
    sub_list = lt.subList(lst, 1, size)
    sorted_list = mgs.sort(sub_list, parameter)
    return sorted_list

# Funciones auxiliares

def listsFusion(lst1, lst2):
    fusionList = lt.newList('ARRAY_LIST')
    for element in lt.iterator(lst1):
        lt.addLast(fusionList, element)
    for element in lt.iterator(lst2):
        lt.addLast(fusionList, element)
    return fusionList

def stringToDateFormat(stringDate):
    if stringDate == '':
        return datetime.datetime.strptime(1,1,1,1,1,1).date()
    else:
        return datetime.datetime.strptime(stringDate, '%Y-%m-%d').date()
