from queue import Queue

def find_start(kaart):
    x, y = (-1, -1)
    for y, scanline in enumerate(kaart):
        x = scanline.find('s')
        if x != -1:
            break
    return None if x == -1 else (x, y)

def get_neighbours(kaart, position):
    neighbours = []
    walls = ['*']
    for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbour = (abs(position[0] + delta[0]), abs(position[1] + delta[1]))
        if neighbour[1] >= len(kaart) or \
                neighbour[0] >= len(kaart[neighbour[1]]) or \
                kaart[neighbour[1]][neighbour[0]] in walls:
            continue
        neighbours.append(neighbour)
    return neighbours

def get_path(came_from, end, start):
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

def map_with_path(map, path, symbol='.'):
    new_map = map.copy()
    keep = ['s', 'D']
    for coord in path:
        str = new_map[coord[1]]
        if str[coord[0]] in keep:
            continue
        new_map[coord[1]] = str[:coord[0]] + symbol + str[coord[0] + 1:]
    return new_map

def minu_otsing(kaart):
    start = find_start(kaart)
    if start is None:
        return []

    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    diamond = None

    while not frontier.empty():
        current = frontier.get()

        if kaart[current[1]][current[0]] == 'D':
            diamond = current
            break

        for next in get_neighbours(kaart, current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return get_path(came_from, diamond, start)


lava_map1 = [
    "      **               **      ",
    "     ***     D        ***      ",
    "     ***                       ",
    "                      *****    ",
    "           ****      ********  ",
    "           ***          *******",
    " **                      ******",
    "*****             ****     *** ",
    "*****              **          ",
    "***                            ",
    "              **         ******",
    "**            ***       *******",
    "***                      ***** ",
    "                               ",
    "                s              ",
]

lava_map2 = [
    "     **********************    ",
    "   *******   D    **********   ",
    "   *******                     ",
    " ****************    **********",
    "***********          ********  ",
    "            *******************",
    " ********    ******************",
    "********                   ****",
    "*****       ************       ",
    "***               *********    ",
    "*      ******      ************",
    "*****************       *******",
    "***      ****            ***** ",
    "                               ",
    "                s              ",
]

lava_map3 = [
    "      **               **      ",
    "     ***     D        ***      ",
    "     ***                       ",
    "                      *****    ",
    "           ****      ********  ",
    "           ***          *******",
    " **                      ******",
    "*****             ****     *** ",
    "*****              **          ",
    "***                            ",
    "s             **         ******",
    "**            ***       *******",
    "***                      ***** ",
    "                               ",
    "                               ",
]

lava_map4 = [
    "     **********************    ",
    "   *******   D    **********   ",
    "   *******                     ",
    " ******************************",
    "***********          ********  ",
    "            *******************",
    " ********    ******************",
    "********                   ****",
    "*****       ************       ",
    "***               *********    ",
    "*      ******      ************",
    "*****************       *******",
    "***      ****            ***** ",
    "                               ",
    "                s              ",
]

lava_map5 = [
    "     ***********    ",
    "   *******   D    ******   ",
    "   ****                     ",
    " *****  **      ",
    "****** *****          ********  ",
    "       *************",
    " ****    *******",
    "********            ****",
    "*****       *       ",
    "***            ***** ****    ",
    "*           ******** * ***",
    "*****      *******   ",
    "***      ****        ***** ",
    "                               ",
    "                s    ",
]
print('Lava map 1 solution')
print('\n'.join(map_with_path(lava_map1, minu_otsing(lava_map1))))
print('Lava map 2 solution')
print('\n'.join(map_with_path(lava_map2, minu_otsing(lava_map2))))
print('Lava map 1 solution with new starting position')
print('\n'.join(map_with_path(lava_map3, minu_otsing(lava_map3))))
print('Lava map 4 (impossible) solution')
print('\n'.join(map_with_path(lava_map4, minu_otsing(lava_map4))))
print('Lava map 5 (variable length) solution')
print('\n'.join(map_with_path(lava_map5, minu_otsing(lava_map5))))
