import copy
class InvalidMoveError(Exception):
    pass
class Board:
    def __init__(self,col,row,k,g):
        self.col = col
        self.row = row
        self.k = k
        self.g = g
        self.board = []
        for i in range(row):
            self.board.append([])
            for j in range(col):
                self.board[i].append(0)

    def make_move(self,move,player):
        if move is None:
            raise InvalidMoveError
        result_board = copy.deepcopy(self)
        if type(move) is tuple:
            move = Move(move[0],move[1])
        if type(player) is not int or (player != 1 and player != 2):
            raise InvalidMoveError()
        if (not self.is_valid_move(move.col,move.row)):
            raise InvalidMoveError()
        if self.g == 0:
            result_board.board[move.row][move.col] = player
        else:
            for i in range(self.row-1,-1,-1):
                if  result_board.board[i][move.col] == 0:
                    result_board.board[i][move.col] = player
                    break
        return result_board

    def is_win(self):
        steps = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        tie = True
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j] == 0:
                    tie = False
                    continue
                first_player = self.board[i][j]
                for step in steps:
                    temp_row = i
                    temp_col = j
                    for _ in range(self.k-1):
                        temp_row += step[0]
                        temp_col += step[1]
                        if (not self.is_valid_move(temp_col,temp_row,False)):
                            break
                        if (self.board[temp_row][temp_col] != first_player):
                            break
                    else:
                        return first_player #wins
        if tie:
            return -1
        return 0




    def show_board(self,fh):
        for i in range(self.row):
            print(i,"|",sep="",end="",file=fh)
            for j in range(self.col):
                print("%3s"%(str(self.board[i][j])),end="",file=fh)
            print(file=fh)
        for j in range(self.col):
            print("----",end="",file=fh)
        print(file=fh)
        print("%2s"%" ",end="",file=fh)
        for j in range(self.col):
            print("%3s"%str(j),end="",file=fh)
        print("\n",file=fh)

    def is_valid_move(self,col,row,check_space=True):
        if col < 0 or col >= self.col:
            return False
        if row < 0 or row >= self.row:
            return False
        if (check_space and self.board[row][col] != 0):
            return False
        return True

class Move:
    def __init__(self,col,row,args=None):
        if type(args) is str:
            self.col,self.row = map(lambda x:int(x),args.split(" "))
            return
        self.col = col
        self.row = row

    @classmethod
    def from_str(cls, s: str):
        """
        This class enables the move object to be made from a str
        @param s: string that describes the class. Eg '(0,0)'
        """
        col,row = map(lambda x:int(x),s.split(" "))
        return cls(col,row)

    def __str__(self):
        return str(self.col)+" "+str(self.row)

