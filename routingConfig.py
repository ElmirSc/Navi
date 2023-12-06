import numpy as np
import math

node_coordinates = np.loadtxt("nodecord.txt")        #laden der nodepl.txt
node_list = np.loadtxt("nodelist.txt").astype(int)     #laden der nodelist.txt und konvertieren der Zahlen zum int für zukünfitge Berrechnungen
arc_list = np.loadtxt("arclist.txt")               #laden der arc_list.txt
node_coordinates_x = []       #array für die longitude Werte
node_coordinates_y = []       #array für die latitude Werte
for cord in node_coordinates:            # abspeichern der lon und lat Werte
 node_coordinates_x.append(cord[0])
 node_coordinates_y.append(cord[1])

costRouteOne = 0
costRouteTwo = 0
costRouteThree = 0