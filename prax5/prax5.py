import sys
sys.path.append('../aima-python-master')
import search


def readMatrixFromFile(path):
    matrix = []
    with (open(path, 'r')) as file:
        file.readline()
        for line in file:
            matrix.append([int(x) for x in line.strip().split(' ')])
    return matrix


def greedy(matrix):
    path = []
    for i in range(len(matrix)):
        best = 99999999999999999
        best_idx = -1
        for j in range(len(matrix)):
            if (i == j): continue
            if best > matrix[i][j] and j not in path:
                best = matrix[i][j]
                best_idx = j
        path.append(best_idx)
    return path


def k_nearest_neighbours(matrix, row, i, k):
    neighbours = []
    for j in range(len(row)):
        if j == i: continue
        best = 999999
        best_idx = -1
        for l, num in enumerate(matrix[j]):
            if num < best and l not in neighbours:
                best = num
                best_idx = l
        neighbours.append(best_idx)
        if len(neighbours) == k:
            break
    return neighbours


class TSP(search.Problem):
    def __init__(self, path, k=None):
        self.matrix = readMatrixFromFile(path)
        self.neighbours = {}
        if k:
            for i in range(len(self.matrix)):
                self.neighbours[i] = k_nearest_neighbours(self.matrix, self.matrix[i], i, k)
        #self.initial = [x for x in range(len(self.matrix))]
        self.initial = greedy(self.matrix)

    # tekitab otsingu algseisu

    def actions(self, state):
        if self.neighbours:
            return [(i, k + 1) for i in range(len(state)) for k in self.neighbours[i]]
        return [(i, k + 1) for i in range(len(state)) for k in range(i, len(state)) if i != k]
    # returnib actionite listi

    def result(self, state, action):
        return state[:action[0]] + list(reversed(state[action[0]:action[1]])) + state[action[1]:]
    # returnib UUE oleku

    def value(self, state):
        val = self.matrix[state[-1]][state[0]]
        prev_city = 0
        for i, city in enumerate(state):
            if i > 0:
                val += self.matrix[prev_city][city]
            prev_city = city
        return -val
# returnib olekule vastava marsruudi pikkuse


problem = TSP('gr48.txt')
g = search.hill_climbing(problem)
print(g)
print(-problem.value(g))
g = search.simulated_annealing(problem)
# muudame SA parameetreid
g = search.simulated_annealing(problem, search.exp_schedule(limit=10000))
print(g)
print(-problem.value(g))
# [9, 10, 2, 14, 13, 16, 5, 7, 6, 12, 3, 0, 15, 11, 8, 4, 1] - gr17 tulemus pikkusega 2085
# [1, 20, 14, 13, 12, 17, 9, 16, 18, 19, 10, 3, 11, 0, 6, 7, 5, 15, 4, 8, 2]
# [13, 14, 20, 1, 2, 8, 4, 15, 5, 7, 6, 0, 11, 3, 10, 19, 18, 16, 9, 17, 12] - gr21 tulemused pikkusega 2707
# [4, 9, 16, 17, 21, 18, 14, 1, 19, 13, 12, 8, 22, 3, 11, 0, 15, 10, 2, 6, 5, 23, 7, 20] - gr24 tulemus pikkusega 1272
