############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Samarth Sanjay Kulkarni"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
import queue as Queue
import random


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    index = 1
    for i in range(rows):
        for j in range(cols):
            board[i][j] = index
            index += 1
    board[rows - 1][cols - 1] = 0
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.__board = board
        self.__rows = len(board)
        self.__cols = len(board[0])
        self.__move = 'none'
        self.attr_1 = 0
        self.attr_2 = 0
        self.attr_3 = 0
        self.route = []
        self.sol = self.solved_board()

        for i in range(self.__rows):
            for j in range(self.__cols):
                if board[i][j] == 0:
                    self.__blank_row = i
                    self.__blank_col = j
                    return

    def set_move(self, move):
        self.__move = move

    def get_move(self):
        return self.__move

    def get_board(self):
        return self.__board

    def perform_move(self, direction):
        if direction == 'up':
            move = [-1, 0]
        if direction == 'down':
            move = [1, 0]
        if direction == 'left':
            move = [0, -1]
        if direction == 'right':
            move = [0, 1]
        pos = [self.__blank_row + move[0], self.__blank_col + move[1]]
        if (pos[0] < 0) or (pos[0] >= self.__rows) or (pos[1] < 0) or (pos[1] >= self.__cols):
            return False
        temp = self.__board[pos[0]][pos[1]]
        self.__board[pos[0]][pos[1]] = 0
        self.__board[self.__blank_row][self.__blank_col] = temp
        self.__blank_row = pos[0]
        self.__blank_col = pos[1]
        return True

    def copy(self):
        return copy.deepcopy(self)

    def convert_to_tuple(self):
        return tuple([tuple(row) for row in self.__board])

    def scramble(self, num_moves):
        for i in range(num_moves):
            self.perform_move(random.choice(['up', 'down', 'left', 'right']))

    def is_solved(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if i == self.__rows - 1 and j == self.__cols - 1:
                    if self.__board[i][j] != 0:
                        return False
                elif self.__board[i][j] != i * self.__cols + j + 1:
                    return False
        return True

    def successors(self):
        for move in ['up', 'down', 'left', 'right']:
            new_puzzle = self.copy()
            if new_puzzle.perform_move(move):
                new_puzzle.set_move(move)
                yield move, new_puzzle

    def solved_board(self):
        board = []
        new = []
        cnt = 1
        for i in range(0, self.__rows):
            for j in range(0, self.__cols):
                new.append(cnt)
                cnt += 1
            board.append(new)
            new = []
        board[self.__rows - 1][self.__cols - 1] = 0
        return board

    # Required
    def find_solutions_iddfs(self):
        is_found_solution = False
        limit = 0
        while not is_found_solution:
            for move in self.find_solution_iddfs_helper(limit, []):
                yield move
                is_found_solution = True
            limit += 1

    def find_solution_iddfs_helper(self, limit, route):
        if self.__board == self.sol:
            yield route
        elif len(route) < limit:
            for move, puzzle in self.successors():
                for sol in puzzle.find_solution_iddfs_helper(limit, route + [move]):
                    yield sol

    # Required
    def find_solution_a_star(self):
        open_set = set()
        closed_set = set()
        open_set.add(self)
        self.attr_1 = self.manhattan_axis(self.sol)
        self.route = []

        while open_set:
            curr = min(open_set, key=lambda x: x.attr_2)

            if curr.__board == self.sol:
                return curr.route
            open_set.remove(curr)

            for move, puzzle in curr.successors():
                if puzzle.__board == self.sol:
                    puzzle.route = curr.route + [move]
                    return puzzle.route

                puzzle.attr_3 = curr.attr_3 + curr.manhattan_axis(puzzle.__board)
                puzzle.attr_1 = puzzle.manhattan_axis(self.sol)
                puzzle.attr_2 = puzzle.attr_3 + puzzle.attr_1

                go = True
                for board in open_set:
                    if board.__board == puzzle.__board and board.attr_2 < puzzle.attr_2:
                        go = False
                        continue
                for board in closed_set:
                    if board.__board == puzzle.__board and board.attr_2 < puzzle.attr_2:
                        go = False
                        continue
                if go:
                    open_set.add(puzzle)
                    puzzle.route = curr.route + [move]

            closed_set.add(curr)

    def manhattan_axis(self, t1):
        total = 0
        pos = {}

        for x in range(self.__rows):
            for y in range(self.__cols):
                pos[t1[x][y]] = (x, y)

        for x in range(self.__rows):
            for y in range(self.__cols):
                a = self.__board[x][y]
                pos2 = pos[a]
                total += abs(x - pos2[0]) + abs(y - pos2[1])
        return total


############################################################
# Section 2: Grid Navigation
############################################################

class GridPuzzle(object):

    def __init__(self, loc):
        self.loc = loc
        self.attr_1 = 0
        self.attr_2 = 0
        self.attr_3 = 0
        self.route = []

    def successors(self, scene):
        x, y = self.loc
        rows = len(scene) - 1
        columns = len(scene[0]) - 1
        if x > 0:
            if not scene[x - 1][y]:
                yield GridPuzzle((x - 1, y))  # up
        if y > 0:
            if not scene[x][y - 1]:
                yield GridPuzzle((x, y - 1))  # left
        if x < rows:
            if not scene[x + 1][y]:
                yield GridPuzzle((x + 1, y))  # down
        if y < columns:
            if not scene[x][y + 1]:
                yield GridPuzzle((x, y + 1))  # right
        if x < rows and y < columns:
            if not scene[x + 1][y + 1]:
                yield GridPuzzle((x + 1, y + 1))  # down-right
        if x < rows and y > 0:
            if not scene[x + 1][y - 1]:
                yield GridPuzzle((x + 1, y - 1))  # down-left
        if x > 0 and y < columns:
            if not scene[x - 1][y + 1]:
                yield GridPuzzle((x - 1, y + 1))  # up-right
        if x > 0 and y > 0:
            if not scene[x - 1][y - 1]:
                yield GridPuzzle((x - 1, y - 1))  # up-left

    def heuristic(self, b):
        x_1, y_1 = self.loc
        x_2, y_2 = b
        return abs(x_1 - x_2) + abs(y_1 - y_2)


def find_path(start, goal, scene):
    open_set = set()
    closed_set = set()
    starting_state = GridPuzzle(start)
    open_set.add(starting_state)
    starting_state.attr_2 = starting_state.heuristic(goal)
    starting_state.route = [start]

    while open_set:
        curr = min(open_set, key=lambda x: x.attr_2)

        if curr.loc == goal:
            return curr.route
        open_set.remove(curr)

        for point in curr.successors(scene):
            if point.loc == goal:
                point.route = curr.route + [point.loc]
                return point.route

            point.attr_1 = curr.attr_1 + curr.heuristic(point.loc)
            point.attr_2 = point.heuristic(goal)
            point.attr_3 = point.attr_1 + point.attr_2

            go = True
            for loc in open_set:
                if loc.loc == point.loc and loc.attr_3 < point.attr_3:
                    go = False
                    continue
            for loc in closed_set:
                if loc.loc == point.loc and loc.attr_3 < point.attr_3:
                    go = False
                    continue
            if go:
                open_set.add(point)
                point.route = curr.route + [point.loc]

        closed_set.add(curr)


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

class LinearDiskMovement(object):

    def __init__(self, n, length, disks):
        self.n = n
        self.length = length
        self.disks = list(disks)
        self.attr_1 = 0
        self.attr_2 = 0
        self.attr_3 = 0
        self.route = []

    def __lt__(self, other):
        return self.attr_1 + self.attr_2 < other.attr_1 + other.attr_2

    def __eq__(self, other):
        return self.disks == other.disks

    def __hash__(self):
        return hash(tuple(self.disks))

    def successors(self):
        for i in range(len(self.disks)):
            if self.disks[i]:
                if i + 1 < self.length:
                    if self.disks[i + 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 1] = disk
                        yield (i, i + 1), LinearDiskMovement(self.n, self.length, replace)

                if i + 2 < self.length:
                    if self.disks[i + 2] == 0 and self.disks[i + 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 2] = disk
                        yield (i, i + 2), LinearDiskMovement(self.n, self.length, replace)

                if i - 1 >= 0:
                    if self.disks[i - 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 1] = disk
                        yield (i, i - 1), LinearDiskMovement(self.n, self.length, replace)

                if i - 2 >= 0:
                    if self.disks[i - 2] == 0 and self.disks[i - 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 2] = disk
                        yield (i, i - 2), LinearDiskMovement(self.n, self.length, replace)

    def heuristic(self, b):
        position = {}
        for i, x in enumerate(b):
            position[x] = i

        total = 0
        for i, x in enumerate(self.disks):
            total += abs(i - position[x])

        return total


def solve_distinct_disks(length, n):
    start = [x + 1 for x in range(n)]
    for x in range(length - n):
        start.append(0)
    goal = list(reversed(copy.deepcopy(start)))

    if start == goal:
        return [()]

    open_set = Queue.PriorityQueue()
    unique_id = 0
    a = LinearDiskMovement(n, length, start)
    open_set.put((a.attr_1 + a.attr_2, unique_id, a))
    unique_id += 1

    while not open_set.empty():
        _, _, curr = open_set.get()

        if curr.disks == goal:
            return curr.route

        for move, disk in curr.successors():
            disk.route = curr.route + [move]
            open_set.put((disk.attr_1 + disk.attr_2, unique_id, disk))
            unique_id += 1

    return None


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board = [[False for x in range(cols)] for y in range(rows)]
    return DominoesGame(board)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.__board = board
        self.row = len(board)
        self.column = len(board[0])

    def get_board(self):
        return self.__board

    def reset(self):
        self.__board = [[False for x in range(self.column)] for y in range(self.row)]

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row + 1 < self.row:
                if not self.__board[row][col] and not self.__board[row + 1][col]:
                    return True
        else:
            if col + 1 < self.column:
                if not self.__board[row][col] and not self.__board[row][col + 1]:
                    return True
        return False

    def legal_moves(self, vertical):
        for row in range(self.row):
            for column in range(self.column):
                if self.is_legal_move(row, column, vertical):
                    yield row, column

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.__board[row][col] = True
                self.__board[row + 1][col] = True
            else:
                self.__board[row][col] = True
                self.__board[row][col + 1] = True

    def game_over(self, vertical):
        return not list(self.legal_moves(vertical))

    def copy(self):
        return copy.deepcopy(self)

    def successors(self, vertical):
        for x, y in list(self.legal_moves(vertical)):
            game = self.copy()
            game.perform_move(x, y, vertical)
            yield (x, y), game

    def get_random_move(self, vertical):
        x = list(self.legal_moves(vertical))
        return random.choice(x)

    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(-float('inf'), float('inf'), None, vertical, limit)

    def max_value(self, alpha, beta, m, vertical, limit):
        verticals = list(self.successors(vertical))
        horizontals = list(self.successors(not vertical))

        if limit == 0 or self.game_over(vertical):
            return m, len(verticals) - len(horizontals), 1

        float_tracker = -float('inf')
        counter = 0
        current_move = m
        for position, child in verticals:
            move, temp, count = child.min_value(alpha, beta, position, not vertical, limit - 1)
            counter += count
            if temp > float_tracker:
                float_tracker = temp
                current_move = position
            if float_tracker >= beta:
                return current_move, float_tracker, counter
            alpha = max(alpha, float_tracker)

        return current_move, float_tracker, counter

    def min_value(self, alpha, beta, m, vertical, limit):
        verticals = list(self.successors(vertical))
        horizontals = list(self.successors(not vertical))

        if limit == 0 or self.game_over(vertical):
            return m, len(horizontals) - len(verticals), 1

        float_tracker = float('inf')
        counter = 0
        current_move = m
        for position, child in verticals:
            move, temp, count = child.max_value(alpha, beta, position, not vertical, limit - 1)
            counter += count
            if temp < float_tracker:
                float_tracker = temp
                current_move = position
            if float_tracker <= alpha:
                return current_move, float_tracker, counter
            beta = min(beta, float_tracker)

        return current_move, float_tracker, counter


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
I spent around 10 finishing the assignment on my first run.
I spent around 4 hours cleaning up the code and making it more efficient after that
Additionally, I spent around 2 hours fixing random bugs and running test cases
In total, I spent a total of 16 hours on this assignment
"""

feedback_question_2 = """
The part I found most challenging was the linear disk movement section. I had to spend a lot of time working out logic, since my code was working for
very limited values of n. I had to go through 4 different iterations before I was able to get it to work for all values of n and length.
"""

feedback_question_3 = """
I enjoyed the grid navigation section the most. I found it to be the most interesting and challenging. I had to spend a lot of time working out the logic,
but the end result was very satisfying.
"""
