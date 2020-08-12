import collections
#initialize board and pies
class TakGame(object):
	def __init__(self, boardsize):
		self.size = boardsize
		self.board = [[[0] for i in range(self.size)]for j in range(self.size)]
		self.pieces, self.capstones = self.getPieces(self.size)
		self.turnCount = 1

	def getPieces(self, size):
		if size == 8:
			cap, pie = 2, 50
		elif size == 7:
			cap, pie = 2, 40
		elif size == 6:
			cap, pie = 1, 30
		elif size == 5:
			cap, pie = 1, 21
		elif size == 4:
			cap, pie = 0, 15
		else:
			cap, pie = 0, 10
		return (pie, cap)

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

	def countRow(self, row):
		count = collections.Counter()
		for col in self.board[row]:
			count = count + collections.Counter(col)
		return count

	def countTotalPieces(self):
		count = collections.Counter()
		for i in range(self.size):
			count = count + self.countRow(i)
		return count

	def isFull(self):
		for row in self.board:
			for col in row:
				if col[-1] == 0:
					return False
		return True

	def outOfPieces(self):
		pC = self.countTotalPieces()
		return (pC[1] == self.pieces and pC[3] == self.capstones) or (pC[-1] == self.pieces and pC[-3] == self.capstones)

	def end(self):
		en = False
		if self.outOfPieces():
			en = True
		elif self.isFull():
			en = True
		elif self.road()[0] or self.road()[1]:
			en = True
		return en

	def isRoadPiece(self, loc, player):
		mod = -1*((-1)**player)
		return self.board[loc[0]][loc[1]][-1] == 1*mod or self.board[loc[0]][loc[1]][-1] == 3*mod

	def isGoal(self, start, loc):
		return (start[0] == 0 and loc[0] == self.size-1) or (start[1] == 0 and loc[1] == self.size-1)

	def checkLoc(self, start, loc, player):
		if self.isGoal(start, loc) and self.isRoadPiece(loc, player):
			return True
		elif self.isRoadPiece(loc, player):
			self.locations.append(loc)
			self.visited[loc[0]][loc[1]] = True
		return False

	def checkRow(self, start, player):
		return self.isRoadPiece([start, 0], player) and self.roadSearch([start, 0], player)

	def checkCol(self, start, player):
		return self.isRoadPiece([0, start], player) and self.roadSearch([0, start], player)

	def roadSearch(self, start, player):
		self.visited = [[False for i in range(self.size)] for j in range(self.size)]
		self.locations = [start]
		self.visited[start[0]][start[1]] = True
		while len(self.locations) > 0:
			check = self.locations.pop(-1)
			adj = self.adjacent(check)
			for loc in adj:
				if not self.visited[loc[0]][loc[1]] and self.checkLoc(start, loc, player):
					return True
		return False

	def road(self):
		p1road, p2road = False, False
		for i in range(self.size):
			if self.checkRow(i, 1) or self.checkCol(i, 1):
				p1road = True
			elif self.checkRow(i, 2) or self.checkCol(i, 2):
				p2road = True
		return p1road, p2road

	def points(self):
		winner = self.winner()
		piecesLeft = self.capstones + self.pieces
		if winner == 1:
			piecesLeft = piecesLeft - (self.countTotalPieces()[1] + self.countTotalPieces()[3])
		else:
			piecesLeft = piecesLeft - (self.countTotalPieces()[-1] + self.countTotalPieces()[-3])
		return (self.size**2) + piecesLeft

	def winRoad(self):
		rd = self.road()
		if rd[0] == True:
			return 1
		elif rd[1] == True:
			return 2
		return False

	def flatStones(self, player):
		flatCount = 0
		for i in range(self.size):
			for j in range(self.size):
				if self.isRoadPiece([i,j], player):
					flatCount += 1
		return flatCount

	def winFlat(self):
		if self.flatStones(1) > self.flatStones(2):
			return 1
		else:
			return 2

	def winner(self):
		if self.winRoad():
			return self.winRoad()
		else:
			return self.winFlat()
