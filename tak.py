import numpy as np, collections
#initialize board and piececounts
def start(size):
	board = [[[0] for i in range(size)]for j in range(size)]
	if size == 8:
		capcount, piececount = 2, 50
		piececount = 50
	elif size == 7:
		capcount, piececount = 2, 40
	elif size == 6:
		capcount, piececount = 1, 30
	elif size == 5:
		capcount, piececount = 1, 21
	elif size == 4:
		capcount, piececount = 0, 15
	else:
		capcount, piececount = 0, 10
	return (board, capcount, piececount)

board, capstones, pieces = start(5)

def adjacent(loc):
	adj = [[loc[0], loc[1]+1], [loc[0], loc[1]-1], [loc[0]+1, loc[1]], [loc[0]-1, loc[1]]]
	return list(filter(onboard, adj))

onboard = lambda loc, b=board: (loc[0] >= 0 and loc[0] < len(b)) and (loc[1] >=0 and loc[1] < len(b))

def end(board = board, capstones=capstones, pieces=pieces):
	end, openSpace = False, False
	pieceCount = [0,0,0,0]
	for row in board:
		for col in row:
			count = collections.Counter(col)
			print(col[-1])
			if col[-1] == 0:
				openSpace = True
			pieceCount[0] += count[1] + count[2]
			pieceCount[1] += count[-1] + count[-2]
			pieceCount[2] += count[3]
			pieceCount[3] += count[-3]
	if (pieceCount[0] == pieces and pieceCount[2] == capstones) or (pieceCount[1] == pieces and pieceCount[3] == capstones):
		end = True
	elif openSpace == False:
		end = True
	return end

def road(board=board):
	visited = [[False for i in range(len(board))] for j in range(len(board))]
	p1 = []
	p2 = []
	for i in range(len(board[0])):
		if board[0][i][-1] == 1 or board[0][i][-1] == 3:
			p1.append([0, i])
			visited[0][i] = True
		elif board[0][i][-1] == -1 or board[0][i][-1] == -3:
			p2.append([0, i])
			visited[0][i] = True
	def roadSearch(startSet, direction, player, board=board):
		mod = -1*((-1)**player)
		while len(startSet) > 0:
			check = startSet.pop(-1)
			adj = adjacent(check)
			for loc in adj:
				if (loc[0] == len(board)-1 and direction == 'V') or (loc[1] == len(board)-1 and direction == 'H'):
					return True
				elif (board[loc[0]][loc[1]][-1] == 1*mod or board[loc[0]][loc[1]][-1] == 3*mod) and not visited[loc[0]][loc[1]]:
					startSet.append(loc)
					visited[loc[0]][loc[1]] = True
		return False
	p1road = roadSearch(p1, 'V', 1)
	p2road = roadSearch(p2, 'V', 2)
	visited = [[False for i in range(len(board))] for j in range(len(board))]
	p1 = []
	p2 = []
	for j in range(0, len(board)):
		if board[j][0][-1] == 1 or board[j][0][-1] == 3:
			p1.append([j, 0])
			visited[j][0] = True
		elif board[j][0][-1] == -1 or board[j][0][-1] == -3:
			p2.append([j, 0])
			visited[j][0] = True
	if p1road is False:
		p1road = roadSearch(p1, 'H', 1)
	if p2road is False:
		p2road = roadSearch(p2, 'H', 2)
	return p1road, p2road
