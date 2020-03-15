from random import randint
from BoardClasses import Move
from BoardClasses import Board
from numpy import array, diag

AI = 1
OP = 2
MAX = 10**9
MIN = -MAX


class StudentAI:
    def __init__(self, col, row, k, g):
        self.k = k
        self.col = col
        self.row = row
        self.board = Board(col, row, k, g)
        self.g = True if g == 1 else False
        self.win = 10 ** k

    def get_move(self, move):
        if move.row == -1 and move.col == -1:
            move = Move(self.col // 2, self.row // 2)
            self.board = self.board.make_move(move, AI)
            return move

        self.board = self.board.make_move(move, OP)

        if self.g: move, _ = self.max_val(self.board.board, MIN, MAX, 6)
        else: move, _ = self.max_val(self.board.board, MIN, MAX, 4)

        while self.board.board[move.row][move.col] != 0:
            move.col = randint(0, self.col - 1)
            move.row = randint(0, self.row - 1)

        self.board = self.board.make_move(move, AI)
        return move

    def available_move(self, board):
        res = []
        for c in range(self.col // 2, self.col):
            for r in range(self.row - 1, -1, -1):
                if board[r][c] == 0:
                    res.append(Move(c, r))
                    if self.g: break
        for c in range(self.col // 2 - 1, -1, -1):
            for r in range(self.row - 1, -1, -1):
                if board[r][c] == 0:
                    res.append(Move(c, r))
                    if self.g: break
        return res

    def max_val(self, board, alpha, beta, deep):
        if deep == 0: return Move(0, 0), self.heuristic(board, AI)
        val = MIN

        res = [Move(0, 0), 0]
        moves = self.available_move(board)

        for mv in moves:
            board[mv.row][mv.col] = AI
            _, score = self.min_val(board, alpha, beta, deep - 1)
            board[mv.row][mv.col] = 0

            if score > val:
                val = score
                res = [mv, score]
                if val >= self.win: break

            alpha = max(alpha, val)
            if alpha >= beta: break
        return res

    def min_val(self, board, alpha, beta, deep):
        if deep == 0: return Move(0, 0), self.heuristic(board, OP)
        val = MAX

        res = [Move(0, 0), 0]
        moves = self.available_move(board)

        for mv in moves:
            board[mv.row][mv.col] = OP
            _, score = self.max_val(board, alpha, beta, deep - 1)
            board[mv.row][mv.col] = 0

            if score < val:
                val = score
                res = [mv, score]
                if val <= -self.win:
                    break

            beta = min(beta, val)
            if alpha >= beta: break
        return res

    def eval(self, board, player):
        val = 0
        for row in board:
            col = len(row)
            j1 = j2 = 0
            while j2 < col:
                space = 0
                while j1 < col and row[j1] != player: j1 += 1
                j2 = j1
                while j2 < col and row[j2] == player: j2 += 1

                if j1 < col and j2 < col:
                    diff = j2 - j1
                    if j1 - 1 > 0 and row[j1 - 1] == 0: space += 1
                    if row[j2] == 0: space += 1
                    if space == 2 and self.g == 0: diff += 1
                    if space != 0: val += 10 ** diff
                    elif self.k == diff: val += 10 ** diff
                elif j1 < col <= j2:
                    diff = col - j1
                    if j1 - 1 >= 0 and row[j1 - 1] == 0: space += 1
                    if space != 0: val += 10 ** diff
                    elif self.k == diff: val += 10 ** diff
                else: break
                j1 = j2
        return val

    def heuristic(self, board1, player):
        def transpose(board):
            return array(board).transpose().tolist()

        def diaganol(board):
            board = array(board)
            res = []
            for i in range(1, len(board)):
                res.append(diag(board, i).tolist())
                res.append(diag(board, -i).tolist())
            res.append(diag(board).tolist())
            return res

        board2 = transpose(board1)
        board3 = diaganol(board1)
        board4 = diaganol(board2)

        val1 = self.eval(board1, AI) + self.eval(board2, AI) + self.eval(board3, AI) + self.eval(board4, AI)
        val2 = self.eval(board1, OP) + self.eval(board2, OP) + self.eval(board3, OP) + self.eval(board4, OP)

        if val1 >= self.win and val2 >= self.win: return self.win if player == AI else -self.win
        if val1 >= self.win or val2 >= self.win: return self.win if val1 >= self.win else -self.win

        return val1 - val2