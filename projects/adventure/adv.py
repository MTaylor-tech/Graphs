from room import Room
from player import Player, QueueLL
from world import World

import random
from ast import literal_eval

# Load world
world = World()


opposite = {'n':'s','s':'n','e':'w','w':'e'}

# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def bfs(g, starting_room):
    q = QueueLL()
    q.enqueue(starting_room)
    visited = []
    shortest = []
    paths = [[starting_room]]
    while q.size > 0:
        cpath = []
        cv = q.dequeue()
        for p in paths:
            if cv in p:
                cpath = p
        visited.append(cv)
        for d in g.get(cv).keys():
            if g.get(cv)[d] == '?':
                return cpath
                # shortest = cpath
                #+ [g.get(cv)[d]]
                break
            if g.get(cv)[d] not in visited:
                paths.append(cpath + [g.get(cv)[d]])
                q.enqueue(g.get(cv)[d])
    return shortest

def first_question(room_dict):
    for direction in room_dict.keys():
        if room_dict.get(direction) == '?':
            return direction
    return None

def retrace(g):
    shortest = bfs(g,player.current_room.id)
    print(shortest)
    for r in shortest:
        if r == '?':
            continue
        for d in g.get(player.current_room.id).keys():
            if g.get(player.current_room.id).get(d)==r:
                player.travel(d)
                traversal_path.append(d)

    # go = traversal_path[:]
    # while len(go) > 0:
    #     backwards = opposite[go.pop()]
    #     player.travel(backwards)
    #     traversal_path.append(backwards)
    #     # print(player.current_room.id)
    #     # print(g.get(player.current_room.id))
    #     for d in g.get(player.current_room.id).keys():
    #         if g[player.current_room.id][d] == '?':
    #             return True

g = {}
v = set()
v.add(player.current_room.id)
while len(v) < len(room_graph):
    if player.current_room.id not in g:
        room_dict = {}
        for e in player.current_room.get_exits():
            room_dict.update({e:'?'})
        g.update({player.current_room.id:room_dict})
    room_dict = g.get(player.current_room.id)
    direction = first_question(room_dict)
    if direction is None:
        retrace(g)
        room_dict = g.get(player.current_room.id)
        direction = first_question(room_dict)
    if direction is None:
        continue
    next_room = player.current_room.get_room_in_direction(direction)
    room_dict.update({direction:next_room.id})
    if next_room.id not in g:
        next_room_dict = {}
        for e in next_room.get_exits():
            if e == opposite[direction]:
                next_room_dict.update({e:player.current_room.id})
            else:
                next_room_dict.update({e:'?'})
        g.update({next_room.id:next_room_dict})
    else:
        g[next_room.id].update({opposite[direction]:player.current_room.id})
        # g.update({player.current_room.id:room_dict})
    if next_room.id not in v:
        v.add(next_room.id)
        traversal_path.append(direction)
        player.travel(direction)

# print(traversal_path)
# print(v)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
