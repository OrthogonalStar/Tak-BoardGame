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

	def roadSearch(self, startSet, direction, player, visited):
		mod = -1*((-1)**player)
		while len(startSet) > 0:
			check = startSet.pop(-1)
			adj = self.adjacent(check)
			for loc in adj:
				if (loc[0] == self.size-1 and direction == 'V') or (loc[1] == self.size-1 and direction == 'H'):
					return True
				elif (self.board[loc[0]][loc[1]][-1] == 1*mod or self.board[loc[0]][loc[1]][-1] == 3*mod) and not visited[loc[0]][loc[1]]:
					startSet.append(loc)
					visited[loc[0]][loc[1]] = True
		return False

	def road(self):
		visited = [[False for i in range(self.size)] for j in range(self.size)]
		p1 = []
		p2 = []
		for i in range(len(self.board[0])):
			if self.board[0][i][-1] == 1 or self.board[0][i][-1] == 3:
				p1.append([0, i])
				visited[0][i] = True
			elif self.board[0][i][-1] == -1 or self.board[0][i][-1] == -3:
				p2.append([0, i])
				visited[0][i] = True
		p1road = self.roadSearch(p1, 'V', 1, visited)
		p2road = self.roadSearch(p2, 'V', 2, visited)
		visited = [[False for i in range(self.size)] for j in range(self.size)]
		p1 = []
		p2 = []
		for j in range(0, self.size):
			if self.board[j][0][-1] == 1 or self.board[j][0][-1] == 3:
				p1.append([j, 0])
				visited[j][0] = True
			elif self.board[j][0][-1] == -1 or self.board[j][0][-1] == -3:
				p2.append([j, 0])
				visited[j][0] = True
		if p1road is False:
			p1road = self.roadSearch(p1, 'H', 1, visited)
		if p2road is False:
			p2road = self.roadSearch(p2, 'H', 2, visited)
		return p1road, p2road
