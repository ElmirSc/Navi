from Routing.routingConfig import *


def dijkstra(start_node, end_node, cost_type):
    permanent_nodes = []  # Array für die Permanent gesetzten Knoten
    temporary_nodes = [start_node]  # Array für die Temporär gesetzten Knoten

    p_j = np.zeros(len(node_list))  # Array für die Vorgängerknoten
    l_j = np.full((len(node_list), 1), np.inf)  # Array für die Gewichtung der Knoten
    l_j[start_node - 1] = 0  # Gewichtung des Startknoten 0 setzen
    r_j = np.full((len(node_list), 1), np.inf)  # Array für die Reichweite der Knoten inf setzen
    r_j[start_node - 1] = 0  # Reichweite des Startknoten 0 setzen

    while len(temporary_nodes) != 0:  # solange die Temporäre Liste nicht leer ist den Algorithmus weiter machen
        v_i, label = get_temporary_node_with_smallest_time(temporary_nodes, l_j)  # den Knoten mit der geringsten Gewichtung nehmen aus den Temporären

        permanent_nodes.append(v_i)  # Knoten mit der geringsten Gewichtung Permanent setzen
        temporary_nodes.remove(v_i)  # jenen Knoten aus der Temporären entfernen

        edge_list = get_edgelist_for_current_node(v_i)  # Arcs vom derzeitig genutzten Knoten herausholen aus der Arcliste

        if edge_list != 0:
            for vj in edge_list:  # für jeden Arc die jeweiligen Knoten setzen
                if look_for_temporary_node(int(vj[0]), temporary_nodes) == 0 and look_for_permanent_node(int(vj[0]),
                                                                                                         permanent_nodes) == 0:  # überprüfung ob der nächste Knoten in keiner der beiden Arrays drin ist

                    l_j[int(vj[0]) - 1] = get_cost_from_edge(vj, cost_type) + l_j[v_i - 1]  # Gewichtung speichern
                    r_j[int(vj[0]) - 1] = get_cost_from_arc(vj) + r_j[v_i - 1]  # Range speichern
                    p_j[int(vj[0]) - 1] = v_i  # den Vorgänger Knoten abspeichern

                    temporary_nodes.append(int(vj[0]))  # Zielknoten der Arc auf Temporär setzen

                if look_for_temporary_node(int(vj[0]), temporary_nodes) == 1 and (
                        get_cost_from_edge(vj, cost_type) + l_j[v_i - 1]) < l_j[int(vj[
                                                                                        0]) - 1]:  # Überprüfen ob sich Zielknoten in der Temporären bereits befindet und ob dessen Gewichtung durch einen anderen Arc verbessert werden würde
                    l_j[int(vj[0]) - 1] = get_cost_from_edge(vj, cost_type) + l_j[
                        v_i - 1]  # setzen der neuen Gewichtung
                    r_j[int(vj[0]) - 1] = get_cost_from_arc(vj) + r_j[v_i - 1]  # setzen der neuen Range
                    p_j[int(vj[0]) - 1] = v_i  # setzen des neuen Vorgängerknoten

    end_range = r_j[end_node - 1]  # Endreichweite filtern

    route = get_route(p_j, start_node, end_node)  # Route von Start bis Ende berrechnen
    return route, end_range


def get_cost_from_arc(arc):  # Range rausfiltern
    return arc[1]


def get_route(p_j, start_node, end_node):  # Routenberrechnung
    route = []
    iteration = end_node
    while start_node != iteration:
        route.append(iteration)
        iteration = int(p_j[iteration - 1])

    route.append(start_node)
    route.reverse()
    return route


def get_cost_from_edge(edge, cost_type):  # Kosten filtern
    return edge[cost_type]


def look_for_temporary_node(node, temporary_node_list):  # Überprüfung ob sich Knoten in Temporären Liste befindet
    for i in range(0, len(temporary_node_list)):
        if temporary_node_list[i] == node:
            return 1
    return 0


def look_for_permanent_node(node, permanent_node_list):  # Überprüfung ob sich Knoten in Permanenten Liste befindet
    for i in range(0, len(permanent_node_list)):
        if permanent_node_list[i] == node:
            return 1
    return 0


def get_temporary_node_with_smallest_time(temporary_nodes, label_list):  # Funktion zum filtern des Knoten mit der geringsten Gewichtung in den Temporären
    if (len(temporary_nodes) == 1):
        return temporary_nodes[0], 0

    smallest_label = 0
    node = 0

    for index in temporary_nodes:
        if smallest_label == 0:
            smallest_label = label_list[index - 1]
            node = index
        elif smallest_label > label_list[index - 1]:
            smallest_label = label_list[index - 1]
            node = index

    return node, smallest_label


def get_edgelist_for_current_node(current_node):  # Arcs vom bestimmten Knoten filtern
    edge_list = []

    if current_node == len(node_list) - 1:
        index_of_next_node = current_node - 1
        range_between_nodes = node_list[current_node - 1] - node_list[index_of_next_node - 1]
        start_node = node_list[current_node - 1]

        for i in range(start_node - range_between_nodes, start_node):
            edge = arc_list[i]
            edge_list.append(edge)

        return edge_list

    index_of_next_node = current_node + 1
    range_between_nodes = node_list[index_of_next_node - 1] - node_list[current_node - 1]

    start_node = node_list[current_node - 1]

    for i in range(start_node - 1, start_node + range_between_nodes - 1):
        edge = arc_list[i]
        edge_list.append(edge)

    return edge_list
