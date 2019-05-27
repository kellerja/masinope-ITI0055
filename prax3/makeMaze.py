size = 900
maze = [' ' * size] * size

maze[0] = 's' + maze[0][1:]
maze[size - 1] = maze[size - 1][:size - 2] + 'D'

with open('{0}x{0}Empty.txt'.format(size), 'w') as file:
    file.writelines([l + '\n' for l in maze])

