import numpy as np

node_list = np.loadtxt("Routing/nodelist.txt").astype(int)  # load nodelist.txt and convert it into integer type
arc_list = np.loadtxt("Routing/arclist.txt")  # load arc_list.txt

# in arclist.txt zeilenummer ist die Kantennummer und erste Zahl ist Ziel und zweite Zahl ist Gewichtung
# in nodelist.txt ist zeilennumer der node und die differenz der Zahl und der Zahl des nächsten Nodes ist die Anzahl der Ziele
