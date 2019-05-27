from queue import Queue, PriorityQueue
from math import sqrt
from timeit import default_timer as timer

START = 's'
END = 'D'
WALL = '*'


def get_neighbours(map_data, position):
    neighbours = []
    walls = ['*']
    for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbour = (abs(position[0] + delta[0]), abs(position[1] + delta[1]))
        if neighbour[1] >= len(map_data) or \
                neighbour[0] >= len(map_data[neighbour[1]]) or \
                map_data[neighbour[1]][neighbour[0]] in walls:
            continue
        neighbours.append(neighbour)
    return neighbours


def h(next, goal):
    return sqrt((goal[0] - next[0]) ** 2 + (goal[1] - next[1]) ** 2)

def h_man(next, goal):
    return abs(goal[0] - next[0]) + abs(goal[1] - next[1])

def bfs(map_data, start, h=None):
    info = {'nodes': 0, 'startTime': timer()}
    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}
    diamond = None
    while not frontier.empty():
        current = frontier.get()
        info['nodes'] += 1
        if map_data[current[1]][current[0]] == END:
            diamond = current
            break
        for next in get_neighbours(map_data, current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    info['endTime'] = timer()
    return came_from, diamond, info


def greedy(map_data, start, h=h):
    info = {'nodes': 0, 'startTime': timer()}
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    goal = find_symbol(map_data, END)
    diamond = None
    while not frontier.empty():
        _, current = frontier.get()
        info['nodes'] += 1
        if map_data[current[1]][current[0]] == END:
            diamond = current
            break
        for next in get_neighbours(map_data, current):
            if next not in came_from:
                priority = h(next, goal)
                frontier.put((priority, next))
                came_from[next] = current
    info['endTime'] = timer()
    return came_from, diamond, info


def a_star(map_data, start, h=h):
    info = {'nodes': 0, 'startTime': timer()}
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    goal = find_symbol(map_data, END)
    diamond = None
    while not frontier.empty():
        _, current = frontier.get()
        info['nodes'] += 1
        if map_data[current[1]][current[0]] == END:
            diamond = current
            break
        for next in get_neighbours(map_data, current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + h(next, goal)
                frontier.put((priority, next))
                came_from[next] = current
    info['endTime'] = timer()
    return came_from, diamond, info


def get_path(came_from, start, end):
    if end is None or \
            start is None or \
            came_from is None or \
            len(came_from) == 0:
        return []
    path = [end]
    while end != start:
        end = came_from[end]
        path.insert(0, end)
    return path


def find_symbol(kaart, symbol=START):
    x, y = (-1, -1)
    for y, scanline in enumerate(kaart):
        x = scanline.find(symbol)
        if x != -1:
            break
    return None if x == -1 else (x, y)


def search(map_data, algorithm=bfs, h=h):
    start = find_symbol(map_data, START)
    if start is None:
        return []
    path_dict, end, info = algorithm(map_data, start, h)
    path = get_path(path_dict, start, end)
    info['pathLength'] = len(path)
    info['deltaTime'] = info['endTime'] - info['startTime']
    return path, info


def map_with_path(map, path, symbol='.'):
    new_map = map.copy()
    keep = [START, END]
    for coord in path:
        str = new_map[coord[1]]
        if str[coord[0]] in keep:
            continue
        new_map[coord[1]] = str[:coord[0]] + symbol + str[coord[0] + 1:]
    return new_map


def load_map(name):
    with open(name, 'r') as file:
        map_data = [l.strip('\n') for l in file.readlines() if len(l) > 1]
    return map_data


def result_to_file(map, name='result.txt'):
    with open(name, 'w') as file:
        file.writelines([l + '\n' for l in map])
