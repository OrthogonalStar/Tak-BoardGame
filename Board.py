class Board(object):

    def __init__(self, size):
        self.size = size
        self.board = [[[0] for i in range(self.size)]for j in range(self.size)]

    def printBoard(self):
        for i in range(self.size):
            print(self.board[i])

    def isAdjacent(self, loc1, loc2):
        return (loc1[0] == loc2[0] and abs(loc1[1] - loc2[1]) == 1) or (loc1[1] == loc2[1] and abs(loc1[0] - loc2[0]) == 1)

    def onboard(self, loc):
        return (loc[0] >= 0 and loc[0] < self.size and (loc[1] >=0 and loc[1] < self.size))

    def adjacent(self, loc):
        adj = [[loc[0], loc[1]+1], [loc[0], loc[1]-1], [loc[0]+1, loc[1]], [loc[0]-1, loc[1]]]
        return list(filter(self.onboard, adj))

    def getTop(self, loc):
        return self.getLocation(loc)[-1]

    def getLocation(self, loc):
        return self.board[loc[0]][loc[1]]

    def countStack(self, loc):
        return len(self.getLocation(loc))

    def isEmpty(self, loc):
        return len(self.getLocation(loc)) ==  1 and self.getTop(loc) == 0
