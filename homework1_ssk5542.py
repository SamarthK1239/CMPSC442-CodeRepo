############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Samarth Sanjay Kulkarni"

############################################################
# Imports
import math
import random
import copy
from collections import deque


############################################################

# Include your imports here, if any are used.


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    f = math.factorial
    return f(n * n) / f(n) / f(n * n - n)


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    pawn_column_row = {}
    ctr = 0
    for column in board:
        # queen in same column
        if column in pawn_column_row:
            return False
        else:
            # queen in diagonal column
            for c, r in pawn_column_row.items():
                if abs(c - column) == abs(r - ctr):
                    return False
                pawn_column_row[column] = ctr
        ctr += 1
    return True


def n_queens_solutions(n):
    solutions = [[]]
    for row in range(n):
        solutions = (solution + [i] for solution in solutions for i in range(n) if n_queens_valid(solution + [i]))
    return solutions


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        # get number of rows and columns
        maxRow = len(self.board)
        maxCol = 0
        # avoid index out of range exception for empty boards
        if maxRow >= 0:
            maxCol = len(self.board[0])
        self.board[row][col] = not self.board[row][col]
        if row - 1 >= 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if col - 1 >= 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        if col + 1 < maxCol:
            self.board[row][col + 1] = not self.board[row][col + 1]
        if row + 1 < maxRow:
            self.board[row + 1][col] = not self.board[row + 1][col]

    def scramble(self):
        maxRow = len(self.board)
        maxCol = 0
        # avoid index out of range exception for empty boards
        if maxRow >= 0:
            maxCol = len(self.board[0])
        for row in range(maxRow):
            for col in range(maxCol):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in self.board:
            for switch in row:
                if switch:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        maxRow = len(self.board)
        maxCol = 0
        # avoid index out of range exception for empty boards
        if maxRow >= 0:
            maxCol = len(self.board[0])
        for row in range(maxRow):
            for col in range(maxCol):
                successor = self.copy()
                successor.perform_move(row, col)
                yield (row, col), successor

    def find_solution(self):
        explored_set = set()
        q = []
        parent = {}
        moves = {}
        parent[self] = self
        moves[self] = (0, 0)
        # final solution containing the appropriate moves
        solution = []
        if self.is_solved():
            return moves[self]
        q.append(self)
        explored_set.add(tuple(tuple(x) for x in self.get_board()))
        while len(q) != 0:
            puzzleInstance = q.pop(0)
            if puzzleInstance.is_solved():
                node = puzzleInstance
                while parent[node] != node:
                    solution.append(moves[node])
                    node = parent[node]
                return list(reversed(solution))
            for move, neighbor in puzzleInstance.successors():
                if tuple(tuple(x) for x in neighbor.get_board()) not in explored_set:
                    parent[neighbor] = puzzleInstance
                    moves[neighbor] = move
                    if neighbor.is_solved():
                        node = neighbor
                        while parent[node] != node:
                            solution.append(moves[node])
                            node = parent[node]
                        return list(reversed(solution))
                    q.append(neighbor)
                    explored_set.add(tuple(tuple(x) for x in neighbor.get_board()))
        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for i in range(cols)] for j in range(rows)])


############################################################
# Section 3: Linear Disk Movement
############################################################
# Write a function solve_identical_disks(length, n) that returns an optimal solution to the above problem as a list of moves, where length is the number of cells in the row
# and n is the number of disks. Each move in the solution should be a two-element tuple of the
# form (from, to) indicating a disk movement from the first cell to the second. As suggested by its
# name, this function should treat all disks as being identical.
# Your solver for this problem should be implemented using a breadth-first graph search. The
# exact solution produced is not important, as long as it is of minimal length.
from collections import deque


def solve_identical_disks(length, n):
    def apply_move(board, i, steps):
        if (i + steps) < 0 or (i + steps) >= length:
            return
        board[i + steps] = board[i]
        board[i] = None

    def successors(board):
        for i, cell in enumerate(board):
            if cell is not None:
                if i + 1 < length and board[i + 1] is None:
                    new_board = list(board[:])
                    apply_move(new_board, i, 1)
                    yield (i, i + 1), new_board

                if i + 2 < length and board[i + 2] is None and board[i + 1] is not None:
                    new_board = list(board[:])
                    apply_move(new_board, i, 2)
                    yield (i, i + 2), new_board

                if i - 1 >= 0 and board[i - 1] is None:
                    new_board = list(board[:])
                    apply_move(new_board, i, -1)
                    yield (i, i - 1), new_board

                if i - 2 >= 0 and board[i - 2] is None and board[i - 1] is not None:
                    new_board = list(board[:])
                    apply_move(new_board, i, -2)
                    yield (i, i - 2), new_board

    def is_solved_identical(board):
        for i in range(length - n):
            if board[i] is not None:
                return False
        return True

    # Explored board states will be stored here.
    explored = set()

    # deque is used. FIFO for BFS.
    q = deque()
    initial_board = [1 if i < n else None for i in range(length)]
    q.append((initial_board, []))  # (board, moves)

    solution = []

    while q:
        board, moves = q.popleft()
        explored.add(tuple(board))

        for move, new_board in successors(board):
            board_tuple = tuple(new_board)
            if board_tuple in explored:
                continue
            new_moves = moves + [move]
            if is_solved_identical(new_board):
                return new_moves
            q.append((new_board, new_moves))

    return None


def apply_move(board, i, steps):
    if (i + steps) < 0 or (i + steps) >= len(board):
        return
    board[i + steps] = board[i]
    board[i] = None


def successors(board):
    for i, cell in enumerate(board):
        if cell is not None:
            if i + 1 < len(board) and board[i + 1] is None:
                new_board = list(board[:])
                apply_move(new_board, i, 1)
                yield (i, i + 1), new_board

            if i + 2 < len(board) and board[i + 2] is None and board[i + 1] is not None:
                new_board = list(board[:])
                apply_move(new_board, i, 2)
                yield (i, i + 2), new_board

            if i - 1 >= 0 and board[i - 1] is None:
                new_board = list(board[:])
                apply_move(new_board, i, -1)
                yield (i, i - 1), new_board

            if i - 2 >= 0 and board[i - 2] is None and board[i - 1] is not None:
                new_board = list(board[:])
                apply_move(new_board, i, -2)
                yield (i, i - 2), new_board


def is_solved_distinct(board, n):
    for i in range(len(board) - n):
        if board[i] is not None:
            return False
    return True


def solve_distinct_disks(length, n):
    def apply_move(board, i, steps):
        if (i + steps) < 0 or (i + steps) >= length:
            return
        board[i + steps] = board[i]
        board[i] = None

    def successors(board):
        for i, cell in enumerate(board):
            if cell is not None:
                if i + 1 < length and board[i + 1] is None:
                    new_board = list(board[:])
                    apply_move(new_board, i, 1)
                    yield (i, i + 1), new_board

                if i + 2 < length and board[i + 2] is None and board[i + 1] is not None:
                    new_board = list(board[:])
                    apply_move(new_board, i, 2)
                    yield (i, i + 2), new_board

                if i - 1 >= 0 and board[i - 1] is None:
                    new_board = list(board[:])
                    apply_move(new_board, i, -1)
                    yield (i, i - 1), new_board

                if i - 2 >= 0 and board[i - 2] is None and board[i - 1] is not None:
                    new_board = list(board[:])
                    apply_move(new_board, i, -2)
                    yield (i, i - 2), new_board

    def is_solved_distinct(board):
        for i in range(length - n):
            if board[i] is not None:
                return False
        return True

    # Explored board states will be stored here.
    explored = set()

    # deque is used. FIFO for BFS.
    q = deque()
    initial_board = [i + 1 if i < n else None for i in range(length)]
    q.append((initial_board, []))  # (board, moves)

    solution = []

    while q:
        board, moves = q.popleft()
        explored.add(tuple(board))

        for move, new_board in successors(board):
            board_tuple = tuple(new_board)
            if board_tuple in explored:
                continue
            new_moves = moves + [move]
            if is_solved_distinct(new_board):
                return new_moves
            q.append((new_board, new_moves))

    return None


print(solve_distinct_disks(4, 3))
############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
