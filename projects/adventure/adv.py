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
    ''' Searches for the shortest path to a new room '''
    q = QueueLL()
    q.enqueue([starting_room])
    visited = []
    shortest = []
    while q.size > 0:
        cpath = q.dequeue()
        cv = cpath[-1]
        visited.append(cv)
        for d in g.get(cv).keys():
            if g.get(cv)[d] == '?':
                if len(shortest)==0:
                    shortest = cpath
                elif len(cpath) < len(shortest):
                    shortest = cpath
            elif g.get(cv)[d] not in visited:
                q.enqueue(cpath+[g.get(cv)[d]])
    return shortest[1:]


def first_question(room_dict):
    ''' Returns the first direction that hasn't been investigated '''
    for direction in room_dict.keys():
        if room_dict.get(direction) == '?':
            return direction
    return None


def random_question(room_dict):
    ''' Returns a random direction that hasn't been investigated '''
    ways = []
    for direction in room_dict.keys():
        if room_dict.get(direction) == '?':
            ways.append(direction)
    if len(ways) > 0:
        return random.choice(ways)
    else:
        return None


def retrace(g, t):
    ''' Used when at a dead end. Goes back to the nearest new room '''
    shortest = bfs(g, player.current_room.id)
    for r in shortest:
        if r == '?':
            continue
        for d in g.get(player.current_room.id).keys():
            if g.get(player.current_room.id).get(d) == r:
                player.travel(d)
                t.append(d)


def find_path():
    ''' The main loop of the program. Traverses the graph. '''
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


x = 1000
y = 0
# Loop through the possible paths to find the shortest.
# This for loop can be adjusted. A higher range will take longer, but has a
# better possibility of finding a shorter path. My best path with this loop is
# 962 moves, which was found on 1000 tries.
for i in range(1000):
# Alternatively, this while loop seeks a path under 960. I achieved a path
# of 959 moves, which took 824 attempts. 'y' is there as an escape so that the
# program doesn't run indefinitely.
# while x > 959 and y < 10000:
    print('.', end=' ')
    traversal = find_path()
    if len(traversal_path)==0 or len(traversal)<len(traversal_path):
        traversal_path = traversal[:]
        x = len(traversal)
    y += 1
print('\n')

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
