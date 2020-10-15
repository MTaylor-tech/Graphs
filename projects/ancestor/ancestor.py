from util import Stack, Queue

def earliest_ancestor(ancestors, starting_node):
    rev_list = build_rev_adj_list(ancestors)
    return bft(rev_list, starting_node)

def build_adj_list(graph):
    adj_list = {}
    for pair in graph:
        source, destination = pair
        if source in adj_list:
            adj_list[source].add(destination)
        else:
            adj_list.update({source:set([destination])})
    # print(adj_list)
    return adj_list

def build_rev_adj_list(graph):
    rev_list = {}
    for pair in graph:
        source, destination = pair
        if destination in rev_list:
            rev_list[destination].add(source)
        else:
            rev_list.update({destination:set([source])})
    return rev_list

def bft(graph, starting_vertex):
    q = Queue()
    q.enqueue(starting_vertex)
    visited = []
    level = 0
    last = [starting_vertex,level]
    printstr = ""
    while q.size() > 0:
        cv = q.dequeue()
        visited.append(cv)
        if graph.get(cv) is not None:
            for n in graph.get(cv):
                if n not in visited:
                    q.enqueue(n)
    if visited[-1]==starting_vertex:
        return -1
    return visited[-1]

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors,6))
