import os, copy

class Game:
    def __init__(self):
        print("inicializada la clase")
        self.n = 8
        self.board = [["2" for x in range(self.n)] for y in range(self.n)]
        self.dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.diry = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.player = None
        self.minEvalBoard = -1  
        self.maxEvalBoard = self.n * self.n + 4 * self.n + 4 + 1  
        self.depth = 4
    
    def getMyVal(self,num):
        if num == "2":
            return "0"
        if num == "1":
            return "2"
        if num == "0":
            return "1"


    def defineBoard(self,boardString):
        myx = 0
        myy = 0
        pieces = list(boardString)
        for piece in pieces:
            self.board[myx][myy] = self.getMyVal(piece)
            if myx == 7:
                myx = -1
                myy = myy + 1
            myx = myx + 1


    def PrintBoard(self):
        m = len(str(self.n - 1))
        for y in range(self.n):
            row = ""
            for x in range(self.n):
                row += self.board[y][x]
                row += " " * m
            print(row + " " + str(y))
        print
        row = ""
        for x in range(self.n):
            row += str(x).zfill(m) + " "
        print(row + "\n")


    def MakeMove(self, board, x, y, player):
        totctr = 0
        board[y][x] = player
        for d in range(8):
            ctr = 0
            for i in range(self.n):
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                if dx < 0 or dx > self.n - 1 or dy < 0 or dy > self.n - 1:
                    ctr = 0
                    break
                elif board[dy][dx] == player:
                    break
                elif board[dy][dx] == "0":
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + self.dirx[d] * (i + 1)
                dy = y + self.diry[d] * (i + 1)
                board[dy][dx] = player
            totctr += ctr
        return (board, totctr)


    def ValidMove(self,board, x, y, player):
        if x < 0 or x > self.n - 1 or y < 0 or y > self.n - 1:
            return False
        if board[y][x] != "0":
            return False
        (boardTemp, totctr) = self.MakeMove(copy.deepcopy(board), x, y, player)
        if totctr == 0:
            return False
        return True

    def EvalBoard(self,board, player):
        tot = 0
        for y in range(self.n):
            for x in range(self.n):
                if board[y][x] == player:
                    if (x == 0 or x == self.n - 1) and (y == 0 or y == self.n - 1):
                        tot += 4
                    elif (x == 0 or x == self.n - 1) or (y == 0 or y == self.n - 1):
                        tot += 2
                    else:
                        tot += 1
        return tot


    def IsTerminalNode(self,board, player):
        for y in range(self.n):
            for x in range(self.n):
                if self.ValidMove(board, x, y, player):
                    return False
        return True


    def GetSortedNodes(self,board, player):
        sortedNodes = []
        for y in range(self.n):
            for x in range(self.n):
                if self.ValidMove(board, x, y, player):
                    (boardTemp, totctr) = self.MakeMove(copy.deepcopy(board), x, y, player)
                    sortedNodes.append((boardTemp, self.EvalBoard(boardTemp, player)))
        sortedNodes = sorted(sortedNodes, key=lambda node: node[1], reverse=True)
        sortedNodes = [node[0] for node in sortedNodes]
        return sortedNodes


    def Minimax(self,board, player, depth, maximizingPlayer):
        if depth == 0 or self.IsTerminalNode(board, player):
            return self.EvalBoard(board, player)
        if maximizingPlayer:
            bestValue = self.minEvalBoard
            for y in range(self.n):
                for x in range(self.n):
                    if self.ValidMove(board, x, y, player):
                        (boardTemp, totctr) = self.MakeMove(copy.deepcopy(board), x, y, player)
                        v = self.Minimax(boardTemp, player, depth - 1, False)
                        bestValue = max(bestValue, v)
        else:  # minimizingPlayer
            bestValue = self.maxEvalBoard
            for y in range(self.n):
                for x in range(self.n):
                    if self.ValidMove(board, x, y, player):
                        (boardTemp, totctr) = self.MakeMove(copy.deepcopy(board), x, y, player)
                        v = self.Minimax(boardTemp, player, depth - 1, True)
                        bestValue = min(bestValue, v)
        return bestValue


    def BestMove(self, board, player):
        maxPoints = 0
        mx = -1
        my = -1
        for y in range(self.n):
            for x in range(self.n):
                if self.ValidMove(board, x, y, player):
                    (boardTemp, totctr) = self.MakeMove(copy.deepcopy(board), x, y, player)
                    points = self.Minimax(boardTemp, player, self.depth, True)
                    if points > maxPoints:
                        maxPoints = points
                        mx = x
                        my = y
        return (mx, my)

    #player 1 turno negras, player 2 turno blancas
    def CalcMove(self,deep, play, board):
        self.depth = deep
        player = play
        self.defineBoard(board)
        (x, y) = self.BestMove(self.board, player)
        if not (x == -1 and y == -1):
            (self.board, totctr) = self.MakeMove(self.board, x, y, player)
            return str(x) + "" + str(y)