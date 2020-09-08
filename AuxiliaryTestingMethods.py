def fillSpace(game, loc, val):
	game.board.board[loc[0]][loc[1]] = [val]

def fillRow(game, row, val):
	for i in range(game.board.size):
		fillSpace(game, [row, i], val)

def fillCol(game, col, val):
	for i in range(game.board.size):
		fillSpace(game, [i, col], val)

def fillBoardEndFull(game):
	for i in range(game.board.size):
		fillRow(game, i, (-1)**i)

def fillBoardEndPiece(game):
	pieces = game.pieces
	capstones = game.capstones
	for i in range(game.board.size):
		for j in range(game.board.size):
			if pieces > 0:
				fillSpace(game, [i, j], 1)
				pieces -= 1
			elif capstones > 0:
				fillSpace(game, [i, j], 3)
				capstones -= 1

def resetBoard(game):
	for i in range(game.board.size):
		fillRow(game, i, 0)
	game.turnCount = 1
