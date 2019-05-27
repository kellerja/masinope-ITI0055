import sys
sys.path.append('../aima-python-master')
import search


class EightPuzzle(search.Problem):

    def actions(self, state): # returnib actionite listi
        for y, s in enumerate(state):
            try:
                x = s.index(0)
                break
            except: continue
        delta = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        actions = []
        for dx, dy in delta:
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx > 2 or ny < 0 or ny > 2:
                continue
            actions.append((nx, ny, x, y))
        return actions

    def result(self, state, action): # returnib UUE oleku
        new_state = list(state)
        num = state[action[1]][action[0]]
        space_l = list(new_state[action[3]])
        space_l[action[2]] = num
        new_state[action[3]] = tuple(space_l)
        num_l = list(new_state[action[1]])
        num_l[action[0]] = 0
        new_state[action[1]] = tuple(num_l)
        return tuple(new_state)

    def goal_test(self, state): # returnib True kui state on lõppolek
        return state == ((1, 2, 3), (4, 5, 6), (7, 8, 0))

    def path_cost(self, c, state1, action, state2):
        return c + 1  # uus cost peale ühe sammu tegemist


inistate = ((1,2,3), (7,0,5), (8,4,6))
goal = ((1,2,3), (4,5,6), (7,8, 0))
problem = EightPuzzle(inistate, goal)
inistate = ((5,4,0), (6,1,8), (7,3,2))
goal = ((1,2,3), (4,5,6), (7,8, 0))
problem2 = EightPuzzle(inistate, goal)
inistate = ((1,8,2), (0,4,3), (7,6,5))
goal = ((1,2,3), (4,5,6), (7,8, 0))
problem3 = EightPuzzle(inistate, goal)
inistate = ((8,6,7), (2,5,4), (3,0,1))
goal = ((1,2,3), (4,5,6), (7,8, 0))
problem4 = EightPuzzle(inistate, goal)
# action, goaltest, result
search.compare_searchers([problem, problem2, problem3, problem4], ["Strateegia", "algolek " + str(((1,2,3), (7,0,5), (8,4,6))), "algolek " + str(((5,4,0), (6,1,8), (7,3,2))), "algolek " + str(((1,8,2), (0,4,3), (7,6,5))), "algolek " + str(((8,6,7), (2,5,4), (3,0,1)))],
                      searchers=[search.breadth_first_search, search.iterative_deepening_search, search.depth_first_graph_search])
