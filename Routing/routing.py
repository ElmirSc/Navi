from Routing.routingConfig import *


def remove_all_edges_with_prev_node_as_target(edge_list, prev_node):
    new_edge_list = []
    for edge in edge_list:
        if edge[0] != prev_node:
            new_edge_list.append(edge)

    if len(new_edge_list) > 0:
        return new_edge_list
    else:
        return edge_list


def dijkstra(start_node, end_node, cost_type, prev_node=None):
    permanent_nodes = []  # array for the permanent nodes
    temporary_nodes = [start_node]  # array for the temporaty nodes

    predecessor_j = np.zeros(len(node_list))  # array for the predecessor nodes
    weight_j = np.full((len(node_list), 1), np.inf)  # array for the weighting of the nodes
    weight_j[start_node - 1] = 0  # setting weight of startnode to zero
    range_j = np.full((len(node_list), 1), np.inf)  # setting in an array the range of every node to inf
    range_j[start_node - 1] = 0  # setting range of startnode to zero

    while len(temporary_nodes) != 0:
        current_node, label = get_temporary_node_with_smallest_range(temporary_nodes,
                                                                     weight_j)  # getting temporary node with the smallest range

        permanent_nodes.append(current_node)  # setting node with the smallest weight to permanent
        temporary_nodes.remove(current_node)

        edge_list = get_edgelist_for_current_node(current_node)  # getting all arcs for the current node

        if prev_node != None:
            edge_list = remove_all_edges_with_prev_node_as_target(edge_list, prev_node)

        if edge_list != 0:
            prev_node = None
            for edge in edge_list:
                if look_for_temporary_node(int(edge[0]), temporary_nodes) == 0 and look_for_permanent_node(int(edge[0]),
                                                                                                           permanent_nodes) == 0:  # überprüfung ob der nächste Knoten in keiner der beiden Arrays drin ist

                    weight_j[int(edge[0]) - 1] = get_cost_from_edge(edge, cost_type) + weight_j[
                        current_node - 1]  # safe weight oft current node
                    range_j[int(edge[0]) - 1] = get_cost_from_arc(edge) + range_j[
                        current_node - 1]  # safe range oft current node
                    predecessor_j[int(edge[0]) - 1] = current_node  # safe predecessor of current node

                    temporary_nodes.append(int(edge[0]))  # setting next node of edge to temporary nodes

                if look_for_temporary_node(int(edge[0]), temporary_nodes) == 1 and (
                        get_cost_from_edge(edge, cost_type) + weight_j[current_node - 1]) < weight_j[int(edge[
                                                                                                             0]) - 1]:  # check if target node is already in temp array and if its weight can be reduced
                    weight_j[int(edge[0]) - 1] = get_cost_from_edge(edge, cost_type) + weight_j[
                        current_node - 1]  # set new weight
                    range_j[int(edge[0]) - 1] = get_cost_from_arc(edge) + range_j[
                        current_node - 1]  # set new range
                    predecessor_j[int(edge[0]) - 1] = current_node  # set new predecessor

    end_range = range_j[end_node - 1]  # getting end range

    route = get_route(predecessor_j, start_node, end_node)  # getting route
    return route, end_range


def get_cost_from_arc(arc):
    return arc[1]


def get_route(p_j, start_node, end_node):  # calc route from start to end
    route = []
    iteration = end_node
    while start_node != iteration:
        route.append(iteration)
        iteration = int(p_j[iteration - 1])

    route.append(start_node)
    route.reverse()
    return route


def get_cost_from_edge(edge, cost_type):  # get cost
    return edge[cost_type]


def look_for_temporary_node(node, temporary_node_list):  # check if node is in temp list
    for i in range(0, len(temporary_node_list)):
        if temporary_node_list[i] == node:
            return 1
    return 0


def look_for_permanent_node(node, permanent_node_list):  # check if node is in permanent list
    for i in range(0, len(permanent_node_list)):
        if permanent_node_list[i] == node:
            return 1
    return 0


def get_temporary_node_with_smallest_range(temporary_nodes,
                                           label_list):
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


def get_edgelist_for_current_node(current_node):
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
