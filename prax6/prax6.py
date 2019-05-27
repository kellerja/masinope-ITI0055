import sys
sys.path.append('../aima-python-master')
import games

infinity = float('inf')


def query_player(game, state):
    """Make a move by querying standard input."""
    moves = game.actions(state)
    all_moves = game.all_moves(state)
    moves_string = " " * (len(str(all_moves[0])) // 2 - 1)
    curr_y = all_moves[0][1]
    for move in all_moves:
        is_move_in_moves = move in moves
        if move[1] == curr_y:
            moves_string += ' ' * (len(str(all_moves[-1][0])) - len(str(move[0])) + len(str(all_moves[-1][1])) - len(str(move[1])) + 1)
        else:
            moves_string += '\n'
            curr_y = move[1]
            if curr_y % 2 == 0:
                moves_string += " " * (len(str(move)) // 2)
        moves_string += str(move) if is_move_in_moves else " " * len(str(move))
    print("available moves:\n{}".format(moves_string))
    move = None
    while moves:
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
        if move not in moves:
            print('Invalid move. Try again')
        else:
            break
    return move


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        if player != state[1]:
            return min_value(state, alpha, beta, depth + 1)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        if player == state[1]:
            return max_value(state, alpha, beta, depth + 1)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


class DotsAndBoxes(games.Game):
    def __init__(self, size=2, players=('A', 'B'), depth=6, padding=0,
                 wall='*', empty=' ', unowned='U', vwall='|', hwall='-'):
        super()
        self.depth = depth
        self.PADDING = padding
        self.WALL = wall
        self.EMPTY = empty
        self.UNOWNED = unowned
        self.PLAYERS = players
        self.WALL_VERTICAL = vwall
        self.WALL_HORIZONTAL = hwall
        self.initial = ([[self.WALL if j % 2 == 0 else self.EMPTY for j in range(size * 2 + 1)] if i % 2 == 0 else [self.EMPTY if j % 2 == 0 else self.UNOWNED for j in range(size * 2 + 1)] for i in range(size * 2 + 1)],
                        self.PLAYERS[0])

    def all_moves(self, state):
        moves = []
        for y in range(len(state[0])):
            for x in range(1 if y % 2 == 0 else 0, len(state[0][y]), 2):
                if state[0][y][x] == self.EMPTY or \
                        state[0][y][x] == self.WALL_HORIZONTAL or \
                        state[0][y][x] == self.WALL_VERTICAL:
                    moves.append((x, y))
        return moves

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        moves = []
        for y in range(len(state[0])):
            for x in range(1 if y % 2 == 0 else 0, len(state[0][y]), 2):
                if state[0][y][x] == self.EMPTY:
                    moves.append((x, y))
        return moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        new_state = ([x.copy() for x in state[0]], self.PLAYERS[0] if state[1] == self.PLAYERS[1] else self.PLAYERS[1])
        new_state[0][move[1]][move[0]] = self.WALL_VERTICAL if move[0] % 2 == 0 else self.WALL_HORIZONTAL
        if new_state[0][move[1]][move[0]] == self.WALL_VERTICAL:
            is_left_captured = [move[0] - 2 >= 0 and new_state[0][move[1]][move[0] - 2] == self.WALL_VERTICAL,
                                move[0] - 1 >= 0 and move[1] - 1 >= 0 and new_state[0][move[1] - 1][move[0] - 1] == self.WALL_HORIZONTAL,
                                True,
                                move[0] - 1 >= 0 and move[1] + 1 < len(new_state[0]) and new_state[0][move[1] + 1][move[0] - 1] == self.WALL_HORIZONTAL
                                ].count(True) == 4
            is_right_captured = [True,
                                 move[1] - 1 >= 0 and move[0] + 1 < len(new_state[0][move[1] - 1]) and new_state[0][move[1] - 1][move[0] + 1] == self.WALL_HORIZONTAL,
                                 move[0] + 2 < len(new_state[0][move[1]]) and new_state[0][move[1]][move[0] + 2] == self.WALL_VERTICAL,
                                 move[1] + 1 < len(state[0]) and move[0] + 1 < len(new_state[0]) and new_state[0][move[1] + 1][move[0] + 1] == self.WALL_HORIZONTAL
                                 ].count(True) == 4
            if is_left_captured:
                new_state[0][move[1]][move[0] - 1] = state[1]
            if is_right_captured:
                new_state[0][move[1]][move[0] + 1] = state[1]
            if is_left_captured or is_right_captured:
                new_state = (new_state[0], state[1])
        else:
            is_top_captured = [move[0] - 1 >= 0 and move[1] - 1 >= 0 and new_state[0][move[1] - 1][move[0] - 1] == self.WALL_VERTICAL,
                               move[1] - 2 >= 0 and new_state[0][move[1] - 2][move[0]] == self.WALL_HORIZONTAL,
                               move[1] - 1 >= 0 and move[0] + 1 < len(new_state[0][move[1] - 1]) and new_state[0][move[1] - 1][move[0] + 1] == self.WALL_VERTICAL,
                               True
                               ].count(True) == 4
            is_bottom_captured = [move[1] + 1 < len(new_state[0]) and move[0] - 1 >= 0 and new_state[0][move[1] + 1][move[0] - 1] == self.WALL_VERTICAL,
                                  True,
                                  move[1] + 1 < len(new_state[0]) and move[0] + 1 < len(new_state[0][move[1] + 1]) and new_state[0][move[1] + 1][move[0] + 1] == self.WALL_VERTICAL,
                                  move[1] + 2 < len(new_state[0]) and new_state[0][move[1] + 2][move[0]] == self.WALL_HORIZONTAL
                                  ].count(True) == 4
            if is_top_captured:
                new_state[0][move[1] - 1][move[0]] = state[1]
            if is_bottom_captured:
                new_state[0][move[1] + 1][move[0]] = state[1]
            if is_top_captured or is_bottom_captured:
                new_state = (new_state[0], state[1])
        return new_state

    def utility(self, state, player):
        value = 0
        for row in state[0]:
            for col in row:
                if col in self.PLAYERS:
                    if col == player:
                        value += 10
                    else:
                        value -= 10
        return value

    def terminal_test(self, state):
        return not self.actions(state)

    def to_move(self, state):
        return state[1]

    def display(self, state):
        print('  ' + ''.join(' ' * self.PADDING + str(i) + ' ' * self.PADDING for i in range(len(state[0]))))
        print('\n'.join([str(i) + ' ' * (len(str(len(state[0]))) - len(str(i))) + ''.join([(' ' if y != self.WALL_HORIZONTAL else self.WALL_HORIZONTAL) * self.PADDING + y + (' ' if y != self.WALL_HORIZONTAL else self.WALL_HORIZONTAL) * self.PADDING + ' ' * (len(str(j)) - 1) for j, y in enumerate(x)]) for i, x in enumerate(state[0])]))
        print('  ' + ''.join(' ' * self.PADDING + str(i) + ' ' * self.PADDING for i in range(len(state[0]))))

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def cutoff(self, state, depth):
        pass

    def eval_fn(self, state):
        pass

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        self.display(state)
        player = None
        move = None
        while not self.terminal_test(state):
            player = self.to_move(state)
            print("Player {} move".format(player), end="")
            if player == self.PLAYERS[0]:
                #print()
                #move = query_player(self, state)
                move = alphabeta_cutoff_search(state, game, self.depth)
                print("d to {}".format(move))
            else:
                move = alphabeta_cutoff_search(state, game, self.depth, None, None)
                print("d to {}".format(move))
            state = self.result(state, move)
            self.display(state)
        print("Player {} moved to {}".format(player, move))
        self.display(state)
        win_util = self.utility(state, self.to_move(self.initial))
        if win_util > 0:
            print("Player {} won!!!!".format(self.to_move(self.initial)))
        elif win_util == 0:
            print("draw")
        else:
            print("Player {} won!!!!".format(self.PLAYERS[0] if self.PLAYERS[0] != self.to_move(self.initial) else self.PLAYERS[1]))
        return win_util

game = DotsAndBoxes(size=7, depth=3, padding=1, unowned=' ')
game.play_game()
