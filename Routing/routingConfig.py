import numpy as np
import math

#node_coordinates = np.loadtxt("Routing/nodecord.txt")        #laden der nodepl.txt
node_list = np.loadtxt("Routing/nodelist.txt").astype(int)     #laden der nodelist.txt und konvertieren der Zahlen zum int für zukünfitge Berrechnungen
arc_list = np.loadtxt("Routing/arclist.txt")               #laden der arc_list.txt
node_coordinates_x = []       #array für die longitude Werte
node_coordinates_y = []       #array für die latitude Werte
drivingInstructions = np.loadtxt("Routing/drivingInstructionsConfig.txt",dtype='str')      #Instruktionen welche richtungen eingeschlagen werden müssen

#for cord in node_coordinates:            # abspeichern der lon und lat Werte
 #node_coordinates_x.append(cord[0])
 #node_coordinates_y.append(cord[1])

costRouteOne = 0
costRouteTwo = 0
costRouteThree = 0

#1 ist die Zeit der Kosten
#2 ist der Weg der Kosten

# in arclist.txt zeilenummer ist die Kantennummer und erste Zahl ist Ziel und zweite Zahl ist Gewichtung
#in nodelist.txt ist zeilennumer der node und die differenz der Zahl und der Zahl des nächsten Nodes ist die Anzahl der Ziele