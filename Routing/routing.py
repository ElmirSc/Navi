from Routing.routingConfig import *

def dijkstra(startNode, endNode, costType):
    permanent_nodes = []        #Array für die Permanent gesetzten Knoten
    temporary_nodes = []        #Array für die Temporär gesetzten Knoten
    temporary_nodes.append(startNode)       #Startknoten wird Temporär gesetzt

    p_j = np.zeros(len(node_list))          #Array für die Vorgängerknoten
    l_j = np.full((len(node_list),1), np.inf)       #Array für die Gewichtung der Knoten
    l_j[startNode-1] = 0        #Gewichtung des Startknoten 0 setzen
    r_j = np.full((len(node_list),1), np.inf)       #Array für die Reichweite der Knoten inf setzen
    r_j[startNode-1] = 0        #Reichweite des Startknoten 0 setzen

    adjecentList = []       #Array für die Arcs

    v_i = startNode
    while len(temporary_nodes) != 0:          #solange die Temporäre Liste nicht leer ist den Algorithmus weiter machen
        v_i, label = getTemporaryNodeWithSmallestTime(temporary_nodes,adjecentList,l_j)             #den Knoten mit der geringsten Gewichtung nehmen aus den Temporären

        permanent_nodes.append(v_i)            #Knoten mit der geringsten Gewichtung Permanent setzen
        temporary_nodes.remove(v_i)            #jenen Knoten aus der Temporären entfernen

        adjecentList = getAdjecentList(v_i,adjecentList)        #Arcs vom derzeitig genutzten Knoten herausholen aus der Arcliste

        if adjecentList != 0:
            for vj in adjecentList:         #für jeden Arc die jeweiligen Knoten setzen
                if lookForTemporaryNode(int(vj[0]), temporary_nodes) == 0 and lookForPermanentNode(int(vj[0]), permanent_nodes) == 0:       #überprüfung ob der nächste Knoten in keiner der beiden Arrays drin ist

                    l_j[int(vj[0]) - 1] = costFunction(vj,costType) + l_j[v_i-1]            #Gewichtung speichern
                    r_j[int(vj[0])-1] = getRange(vj) + r_j[v_i-1]           #Range speichern
                    p_j[int(vj[0]) - 1] = v_i           #den Vorgänger Knoten abspeichern

                    temporary_nodes.append(int(vj[0]))          #Zielknoten der Arc auf Temporär setzen

                if lookForTemporaryNode(int(vj[0]), temporary_nodes) == 1 and (costFunction(vj,costType) + l_j[v_i-1]) < l_j[int(vj[0]) - 1]:           #Überprüfen ob sich Zielknoten in der Temporären bereits befindet und ob dessen Gewichtung durch einen anderen Arc verbessert werden würde
                    l_j[int(vj[0]) - 1] = costFunction(vj,costType) + l_j[v_i-1]        #setzen der neuen Gewichtung
                    r_j[int(vj[0]) - 1] = getRange(vj) + r_j[v_i - 1]       #setzen der neuen Range
                    p_j[int(vj[0]) - 1] = v_i           #setzen des neuen Vorgängerknoten
            #if v_i == endNode:
                #break

    cost = l_j[endNode-1]       #Endkosten filtern
    range = r_j[endNode-1]      #Endreichweite filtern

    # Abspeichern der Daten in .txt
    #with open('data/pricelistDijkstra.txt', 'a') as datei:
    #    datei.write("Startnode: " + str(startNode) + "\tEndnode: " + str(endNode) + "\tTime[h]: " + str(cost) + "\tRange[km]" + str(range) + '\n')

    route = getRoute(l_j,p_j,startNode,endNode)     #Route von Start bis Ende berrechnen
    drivingInstructions = getDrivingInstructions(route)
    return route, range, drivingInstructions


def getRange(arc):          #Range rausfiltern
    return arc[1]

def getRoute(l_j,p_j,startNode,endNode):        #Routenberrechnung
    route = []
    iteration = endNode
    while startNode != iteration:

        route.append(iteration)
        iteration = int(p_j[iteration-1])


    route.append(startNode)

    route.reverse()

    return route

def getNodeFromArcList(arc):        #Zielknoten des Arcs filtern
    return node_list[int(arc[0])-1]

def costFunction(arc, type):        #Kosten filtern
    return arc[type]



def lookForTemporaryNode(node, nodeList):       #Überprüfung ob sich Knoten in Temporären Liste befindet
    for i in range(0,len(nodeList)):
        if nodeList[i] == node:
            return 1

    return 0


def lookForPermanentNode(node, nodeList):       #Überprüfung ob sich Knoten in Permanenten Liste befindet
    for i in range(0, len(nodeList)):
        if nodeList[i] == node:
            return 1

    return 0


def getTemporaryNodeWithSmallestTime(temporaryNodes, list, labelList):          #Funktion zum filtern des Knoten mit der geringsten Gewichtung in den Temporären
    if(len(temporaryNodes) == 1):
        return temporaryNodes[0], 0

    smallestLabel = 0
    node = 0


    for index in temporaryNodes:
        if smallestLabel == 0:
            smallestLabel = labelList[index-1]
            node = index
        elif smallestLabel > labelList[index-1]:
            smallestLabel = labelList[index-1]
            node = index

    return node,smallestLabel



def getIndicesFromList(list,elem):          #index filtern für position vom Knoten
    for i in list:
        if i == np.where(elem == list[i]):
            return i
    return 0

def getSmallestTimeFromArc(node):
    adcList = getAdjecentList(node)
    smallestTimeArc = []
    for arc in adcList:
        if len(smallestTimeArc) == 0:
            smallestTimeArc = arc
        else:
            if smallestTimeArc[1] > arc[1]:
                smallestTimeArc = arc
    return smallestTimeArc

def checkForTemporaryNodes(node,temporaryNodes):          #Überprüfung ob sich Knoten in Temporären Liste befindet
    for tempNode in temporaryNodes:
        if tempNode == node:
            return 1

    return 0


def getAdjecentList(currentNode,oldList):           # Arcs vom bestimmten Knoten filtern
    adjacentList2 = []

    if currentNode == len(node_list)-1:
        indexOfNextNode = currentNode - 1
        rangeArc = node_list[currentNode - 1] - node_list[indexOfNextNode - 1]
        start = node_list[currentNode - 1]

        for i in range(start - rangeArc, start):
            arc = arc_list[i]
            adjacentList2.append(arc)

        return adjacentList2


    indexOfNextNode = currentNode + 1
    rangeArc = node_list[indexOfNextNode-1]-node_list[currentNode-1]

    start = node_list[currentNode-1]

    for i in range(start-1,start + rangeArc-1):
        arc = arc_list[i]
        adjacentList2.append(arc)

    return adjacentList2

def getIndexOfNodeInNodeList(node):             #Index für Knoten in Liste filtern
    for i in range(0,len(node_list)):
        if node == node_list[i]:
            return i
    print("No Node found!!!!")
    return 0

def getDrivingInstructions(route):
    global drivingInstructions
    drivingInstructionsFromRoute = []
    previousNode = 0
    currentNode = 0
    nextNode = 0
    for i in range(len(route)-1):
        if i == 0:
            previousNode = route[i]
            currentNode = route[i]
        else:
            previousNode = route[i-1]
            currentNode = route[i]
        nextNode = route[i+1]
        drivingInstructionsFromRoute.append(findDrivingInstructionInFile(previousNode,currentNode,nextNode))
    return drivingInstructionsFromRoute

def findDrivingInstructionInFile(previousNode,currentNode,nextNode):
    global drivingInstructions
    instruction = 0
    for i in range(len(drivingInstructions)):
        foundPreviousNode = int(drivingInstructions[i][0])
        foundCurrentNode = int(drivingInstructions[i][1])
        foundNextNode = int(drivingInstructions[i][2])
        if foundPreviousNode == previousNode and foundCurrentNode == currentNode and foundNextNode == nextNode:
            instruction = drivingInstructions[i][3]
            break
    return instruction
