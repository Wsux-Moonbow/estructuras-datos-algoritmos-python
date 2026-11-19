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
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import stack as stack
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as mgsort
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Inicialización del catalogo

def newAnalyzer():
    analyzer = {}
    analyzer['ListStations'] = lt.newList('ARRAY_LIST')
    analyzer['listByStation'] = lt.newList('ARRAY_LIST')
    analyzer['MapByJourney'] = mp.newMap(numelements = 100, maptype = "PROBING", loadfactor = 0.5)
    analyzer['MapByStationID'] = mp.newMap(numelements = 700, maptype = "PROBING", loadfactor = 0.5)
    analyzer['MapByStationIDINFO'] = mp.newMap(numelements = 700, maptype = "PROBING", loadfactor = 0.5)
    analyzer['MapByBikeID'] = mp.newMap(numelements = 700, maptype = "PROBING", loadfactor = 0.5)
    analyzer['AuxLtMapInfo'] = lt.newList('ARRAY_LIST')
    analyzer['MapByStationNameToID'] = mp.newMap(numelements = 700, maptype = "PROBING", loadfactor = 0.5)
    analyzer['MapByDate'] = mp.newMap(numelements = 365, maptype = "PROBING", loadfactor = 0.5)
    analyzer['MapByHourRange'] = mp.newMap(numelements = 24, maptype = "PROBING", loadfactor = 0.5)
    analyzer['TripsGraphByCount'] = gr.newGraph(datastructure = 'ADJ_LIST', directed = True, size = 14000)
    analyzer['TripsGraphByTime'] = gr.newGraph(datastructure = 'ADJ_LIST', directed = True, size = 14000)
    analyzer['TripsNoDirectedGraphByTime'] = gr.newGraph(datastructure = 'ADJ_LIST', directed = False, size = 14000)
    analyzer['TripsDateTree'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    return analyzer

# Funciones para agregar informacion al catalogo

'''
if (int(float(journey["Trip  Duration"])) != "") and (int(float(journey["Trip  Duration"])) > 0) and (journey["Start Station Id"] != "") and (journey["End Station Id"] != "") and (journey["End Station Name"] != "") and (journey["Bike Id"] != "") and (int(float(journey["Start Station Id"])) != int(float(journey["End Station Id"]))):
createJourneyMap(analyzer, journey)
addStation(analyzer['TripsGraphByCount'], int(float(journey['Start Station Id'].strip())), int(float(journey['End Station Id'].strip())))
addStation(analyzer['TripsGraphByTime'], int(float(journey['Start Station Id'].strip())), int(float(journey['End Station Id'].strip())))
'''

def addjourney(analyzer, journey):
    deleted = False
    if (journey["Trip  Duration"] == "") or (int(float(journey["Trip  Duration"])) <= 0) or (journey["Start Station Id"] == "") or (journey["End Station Id"] == "") and (journey["End Station Name"] == "") or (journey["Bike Id"] == "") or (int(float(journey["Start Station Id"])) == int(float(journey["End Station Id"]))):
        deleted = True
    else:
        createJourneyMap(analyzer, journey)

    return deleted
# Funciones para creacion de datos

def createJourneyMap(analyzer, journey):

    if journey["Start Station Name"] == "":
        journey["Start Station Name"] = 'Unknown'

    if journey["End Station Name"] == "":
        journey["End Station Name"] = 'Unknown'

    startStationID = addMapByStationID(analyzer,int(float(journey["Start Station Id"])), journey["Start Station Name"])
    endStationID = addMapByStationID(analyzer,int(float(journey["End Station Id"])), journey["End Station Name"])
    journey["Start Station Id"] = startStationID
    journey["End Station Id"] = endStationID
    lt.addLast(analyzer['ListStations'], journey)
    #Agrega el dato de nombre to id
    createIDInfoMap(analyzer['MapByStationIDINFO'], journey["Start Station Name"].strip(), startStationID, journey, True)
    createIDInfoMap(analyzer['MapByStationIDINFO'], journey["End Station Name"].strip(), endStationID, journey, False)
    addMapByNameToConvertToID(analyzer['MapByStationNameToID'], startStationID, journey["Start Station Name"])
    addMapByNameToConvertToID(analyzer['MapByStationNameToID'], endStationID, journey["End Station Name"])
    creatorBikeIDMap(analyzer['MapByBikeID'], journey['Bike Id'], journey)
    keytoAdd = (startStationID, endStationID)

    #Cretion of vertexs
    addStation(analyzer['TripsGraphByCount'], startStationID)
    addStation(analyzer['TripsGraphByCount'], endStationID)
    addStation(analyzer['TripsGraphByTime'], startStationID)
    addStation(analyzer['TripsGraphByTime'], endStationID)
    addStation(analyzer['TripsNoDirectedGraphByTime'], startStationID)
    addStation(analyzer['TripsNoDirectedGraphByTime'], endStationID)

    if journey['User Type'].strip() == "Annual Member":
        createTreeByDate(analyzer, journey)

    if mp.contains(analyzer['MapByJourney'], keytoAdd):
        dicttoChange = me.getValue(mp.get(analyzer['MapByJourney'], keytoAdd))
        dicttoChange['count'] += 1
        dicttoChange['total_time'] += int(journey["Trip  Duration"])
        if journey['User Type'].strip() == "Casual Member":
            dicttoChange['casual'] += 1
        else:
            dicttoChange['annual'] += 1
        #mp.put(analyzer['annual'], keytoAdd, dicttoChange)
    else:
        dict_info = {'count': 1,
                    'total_time': int(float(journey['Trip  Duration'])),
                    'casual': 0,
                    'annual': 0}
        if journey['User Type'].strip() == "Casual Member":
            dict_info['casual'] += 1
        else:
            dict_info['annual'] += 1
        mp.put(analyzer['MapByJourney'], keytoAdd, dict_info)

def createGraphs(analyzer):
    for st1, st2 in lt.iterator(mp.keySet(analyzer['MapByJourney'])):
        journeyDict = me.getValue(mp.get(analyzer['MapByJourney'], (st1, st2)))
        dictStation = me.getValue(mp.get(analyzer['MapByStationIDINFO'], st1))
        entry = mp.get(analyzer['MapByJourney'], (st2, st1))
        average = journeyDict['total_time'] / journeyDict['count']
        if entry:
            journeyDictReverse = me.getValue(entry)
            dictInside1 = me.getValue(mp.get(analyzer['MapByStationIDINFO'],st1))
            dictInside2 = me.getValue(mp.get(analyzer['MapByStationIDINFO'],st2))
            dictInside1['roundTrips'] += 1
            dictInside2['roundTrips'] += 1
            averageReverse = journeyDictReverse['total_time'] / journeyDictReverse['count']
            max = -1
            if average < averageReverse:
                max = average
            else:
                max = averageReverse

            addConnection(analyzer['TripsNoDirectedGraphByTime'], int(st1), int(st2), max)
        listentry = mp.get(analyzer['MapByStationIDINFO'], int(st1))
        if listentry:
            if me.getValue(listentry)['insideLt'] == 0:
                lt.addLast(analyzer['listByStation'], dictStation)
                me.getValue(listentry)['insideLt'] = 1
        addConnection(analyzer['TripsGraphByCount'], int(st1), int(st2), journeyDict['count'])
        addConnection(analyzer['TripsGraphByTime'], int(st1), int(st2), average)
        #createTreeByStartTrips(analyzer,st1)
        #createTreeByStartTrips(analyzer,st2)

def createDateandHourMap(station, journey):
    fulldate = datetime.strptime(journey["Start Time"], '%m/%d/%Y %H:%M')
    day = fulldate.day
    month = fulldate.month
    year = fulldate.year
    onlyDate = str(year) + "-" + "{:02d}".format(month) + "-" + "{:02d}".format(day)
    specificHour = fulldate.hour
    keyRange = hourRangeSelector(specificHour)
    if keyRange:
        creatorCountMap(station['MapByHourRange'], keyRange.strip())
    creatorCountMap(station['MapByDate'], onlyDate)

def addMapByStationID(analyzer, stid, stationType):
    newid = stid + 1000
    new = False
    if mp.contains(analyzer['MapByStationID'], stid):
        if me.getValue(mp.get(analyzer['MapByStationID'], stid)) != stationType:
            while new == False:
                if mp.contains(analyzer['MapByStationID'], newid):
                    if me.getValue(mp.get(analyzer['MapByStationID'], newid)) != stationType:
                        newid += 1000
                    else:
                        new = True
                        return newid
                else:
                    mp.put(analyzer['MapByStationID'], newid, stationType)
                    return newid
        else:
            return stid
    else:
        mp.put(analyzer['MapByStationID'], stid, stationType)
        return stid

def addMapByNameToConvertToID(map, stid, stationName):
    if not mp.contains(map, stationName.replace(" ", "")):
        mp.put(map, stationName.replace(" ", ""), stid)

def addStation(graph, stop):
    """
    Add a vertex to the graph
    """
    if not gr.containsVertex(graph, stop):
        gr.insertVertex(graph, stop)

def addConnection(graph, origin, destination, weight):
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, weight)

def createIDInfoMap(map, name, ID, journey, start):
    ID = int(ID)
    if mp.contains(map, ID):
        dicttoChange = me.getValue(mp.get(map, ID))
        typemap = dicttoChange['types']
        createDateandHourMap(dicttoChange, journey)
        if start:
            lt.addLast(dicttoChange['Out Trips'], journey)
            if journey['User Type'].strip() == "Casual Member":
                count = me.getValue(mp.get(typemap, 'CasualOut'))
                count += 1
                mp.put(typemap,'CasualOut', count)
            else:
                count = me.getValue(mp.get(typemap, 'AnnualOut'))
                count += 1
                mp.put(typemap,'AnnualOut', count)
        else:
            lt.addLast(dicttoChange['In Trips'], journey)
            if journey['User Type'].strip() == "Casual Member":
                count = me.getValue(mp.get(typemap, 'CasualIn'))
                count += 1
                mp.put(typemap,'CasualIn', count)
            else:
                count = me.getValue(mp.get(typemap, 'AnnualIn'))
                count += 1
                mp.put(typemap,'AnnualIn', count)
    else:
        dict_info = {'Station ID':  ID,
                     'Station Name': name.strip(),
                     'Out Trips': lt.newList('ARRAY_LIST'),
                     'In Trips': lt.newList('ARRAY_LIST'),
                     'types': mp.newMap(numelements = 4,  maptype = "PROBING", loadfactor = 0.5),
                     'MapByHourRange': mp.newMap(numelements = 24, maptype = "PROBING", loadfactor = 0.5),
                     'MapByDate': mp.newMap(numelements = 365, maptype = "PROBING", loadfactor = 0.5),
                     'roundTrips': 0,
                     'insideLt':0}

        typemap = dict_info['types']
        mp.put(typemap,'CasualOut', 0)
        mp.put(typemap,'AnnualOut', 0)
        mp.put(typemap,'CasualIn', 0)
        mp.put(typemap,'AnnualIn', 0)
        createDateandHourMap(dict_info, journey)

        if start:
            lt.addLast(dict_info['Out Trips'], journey)
            if journey['User Type'].strip() == "Casual Member":
                count = me.getValue(mp.get(typemap, 'CasualOut'))
                count += 1
                mp.put(typemap,'CasualOut', count)
            else:
                count = me.getValue(mp.get(typemap, 'AnnualOut'))
                count += 1
                mp.put(typemap,'AnnualOut', count)
        else:
            lt.addLast(dict_info['In Trips'], journey)
            if journey['User Type'].strip() == "Casual Member":
                count = me.getValue(mp.get(typemap, 'CasualIn'))
                count += 1
                mp.put(typemap,'CasualIn', count)
            else:
                count = me.getValue(mp.get(typemap, 'AnnualIn'))
                count += 1
                mp.put(typemap,'AnnualIn', count)
        mp.put(map, int(ID), dict_info)

def creatorCountMap(map, key):
    if mp.contains(map, key.strip()):
        value = me.getValue(mp.get(map, key))
        value += 1
        mp.put(map, key, value)
    else:
        count = 1
        mp.put(map, key.strip(), count)

def creatorCountMapINT(map, key):
    if mp.contains(map, key):
        value = me.getValue(mp.get(map, key))
        value += 1
        mp.put(map, key, value)
    else:
        count = 1
        mp.put(map, key, count)

def creatorBikeIDMap(map, bikeID, journey):
    bikeID = int(float(bikeID.strip()))
    if mp.contains(map, bikeID):
        dicttoChange = me.getValue(mp.get(map, bikeID))
        lt.addLast(dicttoChange['trips'], journey)
        dicttoChange['total_time'] += int(journey["Trip  Duration"])
        mp.put(map, bikeID, dicttoChange)
    else:
        dict_info = {'trips': lt.newList('ARRAY_LIST'),
                    'total_time': int(float(journey['Trip  Duration']))}
        lt.addLast(dict_info['trips'], journey)
        mp.put(map, bikeID, dict_info)

def createTreeByStartTrips(analyzer, idStation):
    infoToWork = me.getValue(mp.get(analyzer['MapByStationIDINFO'], idStation))
    howmany = infoToWork['Out Trips']
    if om.contains(analyzer['TripsStartTree'], howmany):
        listSameQuantity = me.getValue(om.get(analyzer['TripsStartTree'], howmany))
        lt.addLast(listSameQuantity, infoToWork)
    else:
        listInCase = lt.newList('ARRAY_LIST')
        lt.addLast(listInCase, infoToWork)
        #om.put(analyzer['TripsStartTree'], howmany, listInCase)

def createTreeByDate(analyzer, journey):
    Fulldate = journey['Start Time']
    #Fulldate = datetime.strptime(str(date), "%m/%d/%Y %H:%M")
    date = Fulldate.split(" ")[0]
    #date = datetime.strptime(date, "%m/%d/%Y")
    if om.contains(analyzer['TripsDateTree'], date):
        listSameQuantity = me.getValue(om.get(analyzer['TripsDateTree'], date))
        lt.addLast(listSameQuantity, journey)
    else:
        listInCase = lt.newList('ARRAY_LIST')
        lt.addLast(listInCase, journey)
        om.put(analyzer['TripsDateTree'], date, listInCase)

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def topFive5Stations(analyzer):
    sortedList = sortLst(analyzer['listByStation'],lt.size(analyzer['listByStation']), cmpFunctionStartedTrips)
    ansLt = lt.subList(sortedList, 1, 5)
    for eachElement in lt.iterator(ansLt):
        eachElement['Out Trips (TOTAL)'] = lt.size(eachElement['Out Trips'])
        eachElement['Suscriber Out Trips'] = me.getValue(mp.get(eachElement['types'], 'AnnualOut'))
        eachElement['Tourist Out Trips'] = me.getValue(mp.get(eachElement['types'], 'CasualOut'))
        eachElement['Out Degree (Routes)'] = gr.outdegree(analyzer['TripsGraphByTime'], eachElement['Station ID'])
        eachElement['Rush hour'] = findMaxLineal(eachElement['MapByHourRange'])
        eachElement['Rush Date'] = findMaxLineal(eachElement['MapByDate'])
    return ansLt

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
def possibleRoutesTimeandSpace(analyzer, startStation, maxTime, minJumps, TOP):
    startStationID = me.getValue(mp.get(analyzer['MapByStationNameToID'], startStation.replace(" ", "")))
    analyzer['pathsTouristRoutes'] = djk.Dijkstra(analyzer['TripsGraphByTime'], startStationID)
    visitedStations = analyzer['pathsTouristRoutes']['visited']
    ltRoutesTime = lt.newList('ARRAY_LIST')
    ltRoutesANS = lt.newList('ARRAY_LIST')
    for station in lt.iterator(mp.keySet(visitedStations)):
        path = djk.pathTo(analyzer['pathsTouristRoutes'], station)
        if (djk.distTo(analyzer['pathsTouristRoutes'], station) <= (maxTime/2)) and (stack.size(path) >= minJumps):
            lt.addLast(ltRoutesTime, (path, djk.distTo(analyzer['pathsTouristRoutes'], station)))
    ansSelected = 0
    for eachPath, weight in lt.iterator(ltRoutesTime):
        if ansSelected == TOP:
            break
        initialQuantityStation = stack.size(eachPath)
        dictAnsw = {}
        dictAnsw['Stop Stations'] = initialQuantityStation
        dictAnsw['Route time [s]'] = round(weight,2)
        dictAnsw['Route time [m]'] = round(weight/60,2)
        dictAnsw['Station IDs'] = ''
        dictAnsw['Station names'] = ''
        iteracion = 0
        while not stack.isEmpty(eachPath):
            search = stack.pop(eachPath)
            id = search['vertexA']
            info = me.getValue(mp.get(analyzer['MapByStationIDINFO'], id))
            if iteracion > 0:
                dictAnsw['Station IDs'] += ' -> '
                dictAnsw['Station names'] += ' -> '
            dictAnsw['Station IDs'] += str(id)
            dictAnsw['Station names'] += info['Station Name']
            iteracion += 1
        lt.addLast(ltRoutesANS, dictAnsw)
        ansSelected += 1
    return lt.size(ltRoutesTime), startStationID, ltRoutesANS

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
def SCComponents(analyzer):
    analyzer['components'] = scc.KosarajuSCC(analyzer['TripsGraphByTime'])
    howMany = scc.connectedComponents(analyzer['components'])
    sscMap = analyzer['components']['idscc']
    mapByComponentInfo = mp.newMap(numelements = howMany, maptype = "PROBING", loadfactor = 0.5)
    anslist = lt.newList('ARRAY_LIST')
    for stationID in lt.iterator(mp.keySet(sscMap)):
        num_component = me.getValue(mp.get(sscMap, stationID))
        #No encuentra el compoennete 0, no se porque >(
        if mp.contains(mapByComponentInfo, num_component):
            lstInside = me.getValue(mp.get(mapByComponentInfo, num_component))
            lt.addLast(lstInside, stationID)

        else:
            stationList = lt.newList()
            lt.addLast(stationList, stationID)
            mp.put(mapByComponentInfo, num_component, stationList)

    for componentNumber in lt.iterator(mp.keySet(mapByComponentInfo)):
        ansdict = {}
        insideVertexList = me.getValue(mp.get(mapByComponentInfo, componentNumber))
        ansdict['SCC Size'] = lt.size(insideVertexList)
        ansdict['SCC ID'] = componentNumber
        ansdict['Max out station trips'] = -1
        ansdict['Max in station trips'] = -1
        for stationID in lt.iterator(insideVertexList):
            stationInfo = me.getValue(mp.get(analyzer['MapByStationIDINFO'], stationID))
            tryIfMaxOUT = lt.size(stationInfo['Out Trips'])
            tryIfMaxIN = lt.size(stationInfo['In Trips'])

            if tryIfMaxOUT > ansdict['Max out station trips']:
                ansdict['Max out station ID'] = stationID
                ansdict['Max out station name'] = stationInfo['Station Name']
                ansdict['Max out station trips'] = tryIfMaxOUT

            if tryIfMaxIN > ansdict['Max in station trips']:
                ansdict['Max in station ID'] = stationID
                ansdict['Max in station name'] = stationInfo['Station Name']
                ansdict['Max in station trips'] = tryIfMaxIN
        lt.addLast(anslist, ansdict)

    sortedAnsList = sortLst(anslist,lt.size(anslist), cmpFunctionSCC)
    return howMany, sortedAnsList

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def quickRoute(analyzer, startStation, endStation):
    startStationID = me.getValue(mp.get(analyzer['MapByStationNameToID'], startStation.replace(" ", "")))
    endStationID = me.getValue(mp.get(analyzer['MapByStationNameToID'], endStation.replace(" ", "")))
    minimumCostPaths(analyzer, startStationID)
    path = minimumCostPath(analyzer, endStationID)
    totaltime = djk.distTo(analyzer['paths'], endStationID)
    listPathAns = lt.newList('ARRAY_LIST')
    size = stack.size(path)
    while not stack.isEmpty(path):
        dictAnsw = {}
        search = stack.pop(path)
        dictAnsw['Start Station ID'] = search['vertexA']
        startIDMap = me.getValue(mp.get(analyzer['MapByStationIDINFO'], search['vertexA']))
        dictAnsw['Start Station Name'] = startIDMap['Station Name']
        dictAnsw['End Station ID'] = search['vertexB']
        endIDMap = me.getValue(mp.get(analyzer['MapByStationIDINFO'], search['vertexB']))
        dictAnsw['End Station Name'] = endIDMap['Station Name']
        dictAnsw['Avg Route Duration'] = search['weight']
        lt.addLast(listPathAns, dictAnsw)
    return startStationID, endStationID, size, totaltime, listPathAns

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=
def routesDateRange(analyzer, startDate, endDate):
    listTrips = lt.newList('ARRAY_LIST')
    ltINTrips = lt.newList('ARRAY_LIST')
    ltOUTTrips = lt.newList('ARRAY_LIST')
    treeToWork = om.values(analyzer['TripsDateTree'], startDate, endDate)
    mapByHourIN = mp.newMap(numelements = 24, maptype = "PROBING", loadfactor = 0.5)
    mapByHourOUT = mp.newMap(numelements = 24, maptype = "PROBING", loadfactor = 0.5)
    for date in lt.iterator(treeToWork):
        for inside in lt.iterator(date):
                lt.addLast(listTrips, inside)

    totalTrips = lt.size(listTrips)
    totalTimeSEC = 0
    stationVisitedMapIn= mp.newMap(numelements = 20, maptype = "PROBING", loadfactor = 0.5)
    stationVisitedMapOut = mp.newMap(numelements = 20, maptype = "PROBING", loadfactor = 0.5)
    stationVisitedMap= mp.newMap(numelements = 20, maptype = "PROBING", loadfactor = 0.5)

    for eachTrips in lt.iterator(listTrips):
        totalTimeSEC += int(float(eachTrips['Trip  Duration']))
        startStation = int(float(eachTrips['Start Station Id']))
        endStation = int(float(eachTrips['End Station Id']))

        #Conteo de estaciones unicas
        if not mp.contains(stationVisitedMap, startStation):
            mp.put(stationVisitedMap, startStation, 'inside')
        if not mp.contains(stationVisitedMap, endStation):
            mp.put(stationVisitedMap, endStation, 'inside')

        #Saco hora de inicio y fin, agrego al mapa de horas especifico si es start o end
        fulldateOUT = datetime.strptime(eachTrips["Start Time"], '%m/%d/%Y %H:%M')
        fulldateIN = datetime.strptime(eachTrips["End Time"], '%m/%d/%Y %H:%M')
        specificHourIN = fulldateIN.hour
        keyRangeIn = hourRangeSelector(specificHourIN)
        if keyRangeIn:
                creatorCountMap(mapByHourIN, keyRangeIn.strip())

        specificHourOUT = fulldateOUT.hour
        keyRangeOUT = hourRangeSelector(specificHourOUT)
        if keyRangeOUT:
                creatorCountMap(mapByHourOUT, keyRangeOUT.strip())

        #Creo mapas para el conteo de max inicio y salida
        creatorCountMapINT(stationVisitedMapOut, startStation)
        creatorCountMapINT(stationVisitedMapIn, endStation)

    totalUniqueStation = mp.size(stationVisitedMap)
    totalTimeHOUR = round(totalTimeSEC/3600, 2)
    keyMaxOutHour, MaxOutHour = findMaxLineal(mapByHourOUT)
    keyMaxInHour, MaxInHour= findMaxLineal(mapByHourIN)

    keyMaxOut, KeyOut = findMaxLineal(stationVisitedMapOut)
    keyMaxIn, KeyIn = findMaxLineal(stationVisitedMapIn)
    OutIDMap = me.getValue(mp.get(analyzer['MapByStationIDINFO'], keyMaxOut))
    InIDMap = me.getValue(mp.get(analyzer['MapByStationIDINFO'], keyMaxIn))

    #Out max
    OutIDMap['Out Trips (TOTAL)'] = me.getValue(mp.get(OutIDMap['types'], "AnnualOut"))
    lt.addLast(ltOUTTrips, OutIDMap)
    #In Max
    InIDMap['In Trips (TOTAL Suscribers)'] = me.getValue(mp.get(OutIDMap['types'], "AnnualIn"))
    lt.addLast(ltINTrips, InIDMap)
    return totalTrips, totalTimeSEC, totalTimeHOUR, totalUniqueStation, ltOUTTrips, ltINTrips, keyMaxOutHour, MaxOutHour, keyMaxInHour, MaxInHour

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 6]  =^..^=    =^..^=    =^..^=    =^..^=
def preventiveBike(analyzer, bikeID):
    bikeInfo = me.getValue(mp.get(analyzer['MapByBikeID'], int(bikeID)))
    ansLtOut = lt.newList('ARRAY_LIST')
    ansLtIn = lt.newList('ARRAY_LIST')
    totalTripsLt = bikeInfo['trips']
    totalTripsDone = lt.size(totalTripsLt)
    totalTripTimeSeconds = bikeInfo['total_time']
    totalTripTimeHours = round(bikeInfo['total_time']/3600 ,1)
    stationVisitedMapIn= mp.newMap(numelements = 20, maptype = "PROBING", loadfactor = 0.5)
    stationVisitedMapOut = mp.newMap(numelements = 20, maptype = "PROBING", loadfactor = 0.5)
    stationVisitedMap= mp.newMap(numelements = 20, maptype = "PROBING", loadfactor = 0.5)
    #insideTripGraph =  gr.newGraph(datastructure = 'ADJ_LIST', directed = True, size = 100)

    for trip in lt.iterator(totalTripsLt):
        startStation = int(float(trip['Start Station Id']))
        endStation = int(float(trip['End Station Id']))
        #addStation(insideTripGraph, startStation)
        #addStation(insideTripGraph, endStation)
        if not mp.contains(stationVisitedMap, startStation):
            mp.put(stationVisitedMap, startStation, 'inside')
        if not mp.contains(stationVisitedMap, endStation):
            mp.put(stationVisitedMap, endStation, 'inside')

        creatorCountMapINT(stationVisitedMapOut, startStation)
        creatorCountMapINT(stationVisitedMapIn, endStation)

    keyMaxOut, MaxOut = findMaxLineal(stationVisitedMapOut)
    keyMaxIn, MaxIn = findMaxLineal(stationVisitedMapIn)
    OutIDMap = me.getValue(mp.get(analyzer['MapByStationIDINFO'], keyMaxOut))
    InIDMap = me.getValue(mp.get(analyzer['MapByStationIDINFO'], keyMaxIn))

    uniqueStation = mp.size(stationVisitedMap)

    #Out Max
    OutIDMap['Out Trips (TOTAL)'] = lt.size(OutIDMap['Out Trips'])
    lt.addLast(ansLtOut, OutIDMap)
    #In Max
    InIDMap['In Trips (TOTAL)'] = lt.size(InIDMap['In Trips'])
    lt.addLast(ansLtIn, InIDMap)

    return totalTripsDone, totalTripTimeSeconds, totalTripTimeHours, uniqueStation, ansLtOut, ansLtIn

# Funciones de consulta
def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['TripsGraphByTime'])
    return scc.connectedComponents(analyzer['TripsGraphByTime'])

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['TripsGraphByTime'], initialStation)
    return analyzer

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

# Funciones auxiliar

def stationSize(analyzer):
    """
    Número de estaciones
    """

    return gr.numVertices(analyzer['TripsGraphByCount'])

def edgesSize(analyzer):
    """
    Número de arcos
    """
    return gr.numEdges(analyzer['TripsGraphByCount'])

def stationSizeND(analyzer):
    """
    Número de estaciones
    """

    return gr.numVertices(analyzer['TripsNoDirectedGraphByTime'])

def edgesSizeND(analyzer):
    """
    Número de arcos
    """
    return gr.numEdges(analyzer['TripsNoDirectedGraphByTime'])

#Funcion de comparacion

def cmpKeysMinToMax(k1, k2):
    if (k1 == k2):
        return 0
    elif (k1 > k2):
        return 1
    else:
        return -1

def cmpFunctionStartedTrips(stationone, stationtwo):
    if int(lt.size(stationone['Out Trips'])) > int(lt.size(stationtwo['Out Trips'])):
        return True
    else:
        return False

def cmpFunctionSCC(stationone, stationtwo):
    if int(stationone['SCC Size']) > int(stationtwo['SCC Size']):
        return True
    elif int(stationone['SCC Size']) == int(stationtwo['SCC Size']):
        if int(stationone['SCC ID']) > int(stationtwo['SCC ID']):
            return True
    else:
        return False

def cmpDates(date1, date2):
    date_format1 = datetime.strptime(str(date1), "%m/%d/%Y %H:%M")
    date_format2 = datetime.strptime(str(date2), "%m/%d/%Y %H:%M")

    if (date_format1 == date_format2):
        return 0
    elif (date_format1 > date_format2):
        return 1
    else:
        return -1

def findMaxLineal(map):
    max = -1
    for key in lt.iterator(mp.keySet(map)):
        element = me.getValue(mp.get(map, key))
        if (element > max):
            max = element
            keymax = key
    return keymax, max

def hourRangeSelector(element):
    range = None
    if 0 <= element < 1:
        range = '0:00 - 0:59'
    elif 1 <= element < 2:
        range = '1:00 - 1:59'
    elif 2 <= element < 3:
        range = '2:00 - 2:59'
    elif 3 <= element < 4:
        range = '3:00 - 3:59'
    elif 4 <= element < 5:
        range = '4:00 - 4:59'
    elif 5 <= element < 6:
        range = '5:00 - 5:59'
    elif 6 <= element < 7:
        range = '6:00 - 6:59'
    elif 7 <= element < 8:
        range = '7:00 - 7:59'
    elif 8 <= element < 9:
        range = '8:00 - 8:59'
    elif 9 <= element < 10:
        range = '9:00 - 9:59'
    elif 10 <= element < 11:
        range = '10:00 - 10:59'
    elif 11 <= element < 12:
        range = '11:00 - 11:59'
    elif 12 <= element < 13:
        range = '12:00 - 12:59'
    elif 13 <= element < 14:
        range = '13:00 - 13:59'
    elif 14 <= element < 15:
        range = '14:00 - 14:59'
    elif 15 <= element < 16:
        range = '15:00 - 15:59'
    elif 16 <= element < 17:
        range = '16:00 - 16:59'
    elif 17 <= element < 18:
        range = '17:00 - 17:59'
    elif 18 <= element < 19:
        range = '18:00 - 18:59'
    elif 19 <= element < 20:
        range = '19:00 - 19:59'
    elif 20 <= element < 21:
        range = '20:00 - 20:59'
    elif 22 <= element < 23:
        range = '22:00 - 22:59'
    elif 23 <= element < 24:
        range = '23:00 - 23:59'
    return range

def listsFusion(lst1, lst2):
    fusionList = lt.newList('ARRAY_LIST')
    for element in lt.iterator(lst1):
        lt.addLast(fusionList, element)
    for element in lt.iterator(lst2):
        lt.addLast(fusionList, element)
    return fusionList

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

def newInfoDG(analyzer, ID):
    dictInfo = me.getValue(mp.get(analyzer['MapByStationIDINFO'], int(ID)))
    dictInfo['In Degree (Routes)'] = gr.indegree(analyzer['TripsGraphByTime'], ID)
    dictInfo['Out Degree (Routes)'] = gr.outdegree(analyzer['TripsGraphByTime'], ID)
    dictInfo['Out Trips (TOTAL)'] = lt.size(dictInfo['Out Trips'])
    dictInfo['In Trips (TOTAL)'] = lt.size(dictInfo['In Trips'])
    return dictInfo

def newInfoND(analyzer, ID):
    dictInfo = me.getValue(mp.get(analyzer['MapByStationIDINFO'], int(ID)))
    dictInfo['Degree (Rep Routes)'] = gr.degree(analyzer['TripsNoDirectedGraphByTime'], ID)
    return dictInfo

def answerLst(fifaList, num = 3):
    if lt.size(fifaList) <= num * 2:
        return fifaList
    else:
        firsts = getFirstNum(num, fifaList)
        lasts = getLastNum(num, fifaList)
        return listsFusion(firsts, lasts)

def answerListLoading(analyzer):
    lth = answerLst(analyzer['ListStations'], 5)
    answerListDG = lt.newList('ARRAY_LIST')
    answerListND = lt.newList('ARRAY_LIST')
    for ansJourney in lt.iterator(lth):
        lt.addLast(answerListDG, newInfoDG(analyzer, ansJourney['Start Station Id']))
        lt.addLast(answerListND, newInfoND(analyzer, ansJourney['Start Station Id']))
    return answerListDG, answerListND

def sortLst(lst, size, parameter):
    sub_list = lt.subList(lst, 1, size)
    sub_list = sub_list.copy()
    sorted_list = mgsort.sort(sub_list, parameter)
    return sorted_list