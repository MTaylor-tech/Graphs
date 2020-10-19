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
    q.enqueue([starting_room])
    # e = g[starting_room]
    # print(e)
    # x = {}
    # for ex in e.keys():
    #     # print(ex)
    #     x.update({e.get(ex):ex})
    # print(x)
    visited = []
    v = {}
    shortest = []
    # paths = [[starting_room]]
    while q.size > 0:
        cpath = q.dequeue()
        cv = cpath[-1]
        # cpath = []
        # cv = q.dequeue()
        # for p in paths:
        #     if cv in p:
        #         cpath = p
        visited.append(cv)
        # print(visited)
        for d in g.get(cv).keys():
            if g.get(cv)[d] == '?':
                # if len(visited) > 1 and cv in x:
                #     return [x.get(cv),d]
                # return cpath[1:]
                # # shortest = cpath
                # #+ [g.get(cv)[d]]
                # break
                if len(shortest)==0:
                    shortest = cpath
                elif len(cpath) < len(shortest):
                    shortest = cpath
            elif g.get(cv)[d] not in visited:
                # paths.append(cpath + [g.get(cv)[d]])
                # q.enqueue(g.get(cv)[d])
                q.enqueue(cpath+[g.get(cv)[d]])
    return shortest[1:]

def first_question(room_dict):
    for direction in room_dict.keys():
        if room_dict.get(direction) == '?':
            return direction
    return None

def random_question(room_dict):
    ways = []
    for direction in room_dict.keys():
        if room_dict.get(direction) == '?':
            ways.append(direction)
    if len(ways) > 0:
        return random.choice(ways)
    else:
        return None

def retrace(g,t):
    shortest = bfs(g,player.current_room.id)
    # print(shortest)
    for r in shortest:
        if r == '?':
            continue
        for d in g.get(player.current_room.id).keys():
            if g.get(player.current_room.id).get(d)==r:
                player.travel(d)
                t.append(d)

def find_path():
    g = {}
    traversal = []
    player.current_room = world.starting_room
    v = set()
    v.add(player.current_room.id)
    while len(v) < len(room_graph):
        if player.current_room.id not in g:
            room_dict = {}
            for e in player.current_room.get_exits():
                room_dict.update({e:'?'})
            g.update({player.current_room.id:room_dict})
        room_dict = g.get(player.current_room.id)
        direction = random_question(room_dict)
        if direction is None:
            retrace(g,traversal)
            room_dict = g.get(player.current_room.id)
            direction = random_question(room_dict)
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
            traversal.append(direction)
            player.travel(direction)
    return traversal

# print(traversal_path)
# print(v)
for i in range(1000):
    print('.',end=' ')
    traversal = find_path()
    if len(traversal_path)==0 or len(traversal)<len(traversal_path):
        traversal_path = traversal[:]
print('\n')
# traversal_path = find_path()
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
